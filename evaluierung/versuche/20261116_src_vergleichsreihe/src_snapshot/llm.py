from langchain_openai import ChatOpenAI


# Erstellt die Modellanbindung mit Projektwerten oder übergebenen Einstellungen.
def get_llm(
    modell_name: str,
    api: str | None = None,
    *,
    base_url: str | None = None,
    temperature: float | None = None,
    timeout: float | None = None,
    max_retries: int = 2,
    max_tokens: int | None = None,
) -> ChatOpenAI:
    from config.meta_config import (
        API_KEY,
        KICONNECT_BASE_URL,
        LLM_TEMPERATURE,
        LLM_TIMEOUT_SECONDS,
    )

    api_key = api or API_KEY
    if not api_key:
        raise ValueError("API Key fehlt.")

    return ChatOpenAI(
        model=modell_name,
        api_key=api_key,
        base_url=(
            KICONNECT_BASE_URL if base_url is None else base_url
        ),
        temperature=(
            LLM_TEMPERATURE if temperature is None else temperature
        ),
        timeout=(
            LLM_TIMEOUT_SECONDS if timeout is None else timeout
        ),
        max_retries=max_retries,
        max_tokens=max_tokens,
    )