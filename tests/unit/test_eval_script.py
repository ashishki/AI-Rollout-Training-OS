from pathlib import Path

import scripts.eval as eval_script
from ai_rollout_os.core.config import Settings


def test_main_passes_no_write_markdown_flag_to_run_evaluation(monkeypatch) -> None:
    observed: dict[str, bool] = {}

    def fake_run_evaluation(**kwargs):
        observed["write_markdown"] = kwargs["write_markdown"]
        return eval_script.EvaluationMetrics(
            hit_at_3=1.0,
            hit_at_5=1.0,
            mrr=1.0,
            citation_precision=1.0,
            no_answer_accuracy=1.0,
            citation_field_presence=1.0,
            median_retrieval_latency_ms=1.0,
            p95_retrieval_latency_ms=1.0,
            query_count=10,
        )

    monkeypatch.setattr(eval_script, "run_evaluation", fake_run_evaluation)
    monkeypatch.setattr(eval_script, "create_engine", lambda _url: object())
    monkeypatch.setattr(eval_script, "ensure_database_schema", lambda _url: None)
    monkeypatch.setattr(
        eval_script,
        "load_settings",
        lambda: Settings(database_url="postgresql+psycopg://example/test"),
    )

    exit_code = eval_script.main(
        [
            "--no-write",
            "--eval-doc",
            str(Path("docs/retrieval_eval.md")),
            "--fixture",
            str(Path("tests/fixtures/seed_training_documents.json")),
        ]
    )

    assert exit_code == 0
    assert observed["write_markdown"] is False


def test_eval_uses_stub_embeddings_for_test_keys() -> None:
    client = eval_script.select_embedding_client(
        Settings(ai_provider_api_key="test-key")
    )

    assert isinstance(client, eval_script.DeterministicEvalEmbeddingClient)
    assert client.model.startswith("test-")
