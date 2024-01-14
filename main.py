from whatsapp_scraper import WhatsAppScraper


def main():
    try:
        scraper = WhatsAppScraper()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            scraper.cleanup()
        except UnboundLocalError:
            pass


if __name__ == "__main__":
    main()
