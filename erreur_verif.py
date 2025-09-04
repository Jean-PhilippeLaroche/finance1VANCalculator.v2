from rich.prompt import Prompt

def input_retry(prompt, type_cast = str, max_retries = None):
    attempts = 0
    while True:
        try:
            value = type_cast(Prompt.ask(prompt))
            return value
        except Exception as e:
            print(f"Erreur de valeur: {e}. Réessayez.")
            attempts += 1
            if max_retries is not None and attempts >= max_retries:
                raise