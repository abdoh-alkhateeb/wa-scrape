import traceback
from whatsapp_scraper import WhatsAppScraper


def main():
    try:
        scraper = WhatsAppScraper()
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()
    finally:
        try:
            scraper.cleanup()
        except UnboundLocalError:
            WhatsAppScraper.deflate_session_file()


if __name__ == "__main__":
    main()
