"""
Unit tests and integration tests for MiniMax provider support.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config_manager import PROVIDERS, get_config, save_config, get_models_for_provider
from models import (
    MODEL_REGISTRY,
    ModelSpec,
    get_models_by_provider,
    get_models_by_capability,
    get_model,
    get_best_model_for_task,
    format_context_window,
)
from chat import chat_request


# =============================================================================
# config_manager tests
# =============================================================================

class TestMiniMaxProviderConfig(unittest.TestCase):
    """MiniMax provider entry in PROVIDERS dict."""

    def test_minimax_in_providers(self):
        self.assertIn("minimax", PROVIDERS)

    def test_minimax_name(self):
        self.assertEqual(PROVIDERS["minimax"]["name"], "MiniMax")

    def test_minimax_url(self):
        self.assertEqual(PROVIDERS["minimax"]["url"], "https://platform.minimaxi.com")

    def test_minimax_models_list(self):
        models = PROVIDERS["minimax"]["models"]
        self.assertIn("MiniMax-M2.5", models)
        self.assertIn("MiniMax-M2.5-highspeed", models)
        self.assertEqual(len(models), 2)

    def test_get_models_for_minimax(self):
        models = get_models_for_provider("minimax")
        self.assertEqual(models, ["MiniMax-M2.5", "MiniMax-M2.5-highspeed"])

    def test_all_providers_have_required_keys(self):
        for pid, pdata in PROVIDERS.items():
            self.assertIn("name", pdata, f"{pid} missing 'name'")
            self.assertIn("url", pdata, f"{pid} missing 'url'")
            self.assertIn("models", pdata, f"{pid} missing 'models'")


# =============================================================================
# models.py tests
# =============================================================================

class TestMiniMaxModelRegistry(unittest.TestCase):
    """MiniMax model entries in MODEL_REGISTRY."""

    def test_m25_in_registry(self):
        self.assertIn("MiniMax-M2.5", MODEL_REGISTRY)

    def test_m25_highspeed_in_registry(self):
        self.assertIn("MiniMax-M2.5-highspeed", MODEL_REGISTRY)

    def test_m25_provider(self):
        spec = MODEL_REGISTRY["MiniMax-M2.5"]
        self.assertEqual(spec.provider, "minimax")

    def test_m25_context_window(self):
        spec = MODEL_REGISTRY["MiniMax-M2.5"]
        self.assertEqual(spec.context_window, 204800)

    def test_m25_capabilities(self):
        spec = MODEL_REGISTRY["MiniMax-M2.5"]
        self.assertIn("chat", spec.capabilities)
        self.assertIn("code", spec.capabilities)
        self.assertIn("reasoning", spec.capabilities)
        self.assertIn("long-context", spec.capabilities)

    def test_m25_highspeed_provider(self):
        spec = MODEL_REGISTRY["MiniMax-M2.5-highspeed"]
        self.assertEqual(spec.provider, "minimax")

    def test_m25_highspeed_context(self):
        spec = MODEL_REGISTRY["MiniMax-M2.5-highspeed"]
        self.assertEqual(spec.context_window, 204800)

    def test_get_models_by_provider_minimax(self):
        models = get_models_by_provider("minimax")
        ids = [m.model_id for m in models]
        self.assertIn("MiniMax-M2.5", ids)
        self.assertIn("MiniMax-M2.5-highspeed", ids)
        self.assertEqual(len(ids), 2)

    def test_get_model_m25(self):
        spec = get_model("MiniMax-M2.5")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.display_name, "MiniMax M2.5")

    def test_get_model_m25_highspeed(self):
        spec = get_model("MiniMax-M2.5-highspeed")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.display_name, "MiniMax M2.5 Highspeed")

    def test_minimax_models_have_code_capability(self):
        models = get_models_by_provider("minimax")
        for m in models:
            self.assertIn("code", m.capabilities, f"{m.model_id} missing 'code'")

    def test_best_model_for_code_minimax(self):
        best = get_best_model_for_task("code", provider="minimax")
        self.assertIsNotNone(best)
        self.assertEqual(best.provider, "minimax")

    def test_format_context_window_204k(self):
        result = format_context_window(204800)
        self.assertIn("K", result)


# =============================================================================
# chat.py tests
# =============================================================================

class TestMiniMaxChatRequest(unittest.TestCase):
    """chat_request() with minimax provider."""

    def test_missing_api_key(self):
        result = chat_request([], "", "minimax", "MiniMax-M2.5")
        self.assertIn("Error", result)

    def test_empty_api_key(self):
        result = chat_request([], "   ", "minimax", "MiniMax-M2.5")
        self.assertIn("Error", result)

    @patch("requests.post")
    def test_successful_request(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello!"}}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        messages = [{"role": "user", "content": "Hi"}]
        result = chat_request(messages, "test-key", "minimax", "MiniMax-M2.5")

        self.assertEqual(result, "Hello!")
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], "https://api.minimax.io/v1/chat/completions")
        self.assertEqual(call_args[1]["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(call_args[1]["json"]["model"], "MiniMax-M2.5")

    @patch("requests.post")
    def test_minimax_url(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": "ok"}}]}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        chat_request([{"role": "user", "content": "test"}], "key", "minimax", "MiniMax-M2.5")

        url = mock_post.call_args[0][0]
        self.assertEqual(url, "https://api.minimax.io/v1/chat/completions")

    @patch("requests.post")
    def test_highspeed_model(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": "fast"}}]}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = chat_request(
            [{"role": "user", "content": "test"}],
            "key",
            "minimax",
            "MiniMax-M2.5-highspeed",
        )
        self.assertEqual(result, "fast")
        payload = mock_post.call_args[1]["json"]
        self.assertEqual(payload["model"], "MiniMax-M2.5-highspeed")

    @patch("requests.post")
    def test_api_error_handling(self, mock_post):
        import requests as real_requests

        mock_post.side_effect = real_requests.exceptions.ConnectionError("timeout")

        result = chat_request(
            [{"role": "user", "content": "test"}], "key", "minimax", "MiniMax-M2.5"
        )
        self.assertIn("API Error", result)

    @patch("requests.post")
    def test_empty_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": ""}}]}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = chat_request(
            [{"role": "user", "content": "test"}], "key", "minimax", "MiniMax-M2.5"
        )
        self.assertEqual(result, "[Empty response]")

    def test_unknown_provider(self):
        result = chat_request([], "key", "unknown_provider", "model")
        self.assertIn("Error", result)


# =============================================================================
# Config persistence tests
# =============================================================================

class TestMiniMaxConfigPersistence(unittest.TestCase):
    """Config save/load with minimax provider."""

    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), ".test_config")
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file = os.path.join(self.test_dir, "config.json")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    @patch("config_manager.CONFIG_DIR")
    @patch("config_manager.CONFIG_FILE")
    def test_save_and_load_minimax(self, mock_file, mock_dir):
        mock_dir.__str__ = lambda s: self.test_dir
        mock_file.__str__ = lambda s: self.test_file

        import config_manager
        orig_dir = config_manager.CONFIG_DIR
        orig_file = config_manager.CONFIG_FILE
        config_manager.CONFIG_DIR = self.test_dir
        config_manager.CONFIG_FILE = self.test_file
        try:
            save_config("minimax", "MiniMax-M2.5", "test-api-key")
            cfg = get_config()
            self.assertEqual(cfg["provider"], "minimax")
            self.assertEqual(cfg["model"], "MiniMax-M2.5")
            self.assertEqual(cfg["api_key"], "test-api-key")
        finally:
            config_manager.CONFIG_DIR = orig_dir
            config_manager.CONFIG_FILE = orig_file


# =============================================================================
# Integration tests (require MINIMAX_API_KEY)
# =============================================================================

@unittest.skipUnless(
    os.getenv("MINIMAX_API_KEY"),
    "Requires MINIMAX_API_KEY environment variable"
)
class TestMiniMaxIntegration(unittest.TestCase):
    """MiniMax API integration tests with real API calls."""

    def test_simple_chat(self):
        """Test a basic chat completion via MiniMax API."""
        api_key = os.environ["MINIMAX_API_KEY"]
        messages = [{"role": "user", "content": "Reply with exactly: OK"}]
        result = chat_request(messages, api_key, "minimax", "MiniMax-M2.5")
        self.assertNotIn("[Error]", result)
        self.assertNotIn("[API Error]", result)
        self.assertTrue(len(result) > 0)

    def test_highspeed_model(self):
        """Test chat completion with M2.5-highspeed model."""
        api_key = os.environ["MINIMAX_API_KEY"]
        messages = [{"role": "user", "content": "What is 2+2? Answer with just the number."}]
        result = chat_request(messages, api_key, "minimax", "MiniMax-M2.5-highspeed")
        self.assertNotIn("[Error]", result)
        self.assertTrue(len(result) > 0)

    def test_multi_turn_conversation(self):
        """Test multi-turn conversation works correctly."""
        api_key = os.environ["MINIMAX_API_KEY"]
        messages = [
            {"role": "user", "content": "My name is TestBot."},
            {"role": "assistant", "content": "Nice to meet you, TestBot!"},
            {"role": "user", "content": "What is my name?"},
        ]
        result = chat_request(messages, api_key, "minimax", "MiniMax-M2.5")
        self.assertNotIn("[Error]", result)
        self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()
