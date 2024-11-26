from system.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    print(settings.model_dump())
