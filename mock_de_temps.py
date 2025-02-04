
from playwright.sync_api import sync_playwright


def mock_conduit_time():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=30000)
        context = browser.new_context()

        # 📌 Mocker l'heure dans Playwright (JavaScript)
        context.add_init_script("""
            const originalDate = Date;
            class MockDate extends originalDate {
                constructor(...args) {
                    if (args.length === 0) {
                        super('2027-01-01T00:00:00Z');  // 🕛 Date forcée
                    } else {
                        super(...args);
                    }
                }
            }
            window.Date = MockDate;
        """)

        page = context.new_page()
        page.goto("https://conduit.bondaracademy.com/")

        print("✅ Mock de temps appliqué avec succès !")
        page.evaluate("console.log(new Date());")  # Vérifier la date dans la console

        browser.close()

mock_conduit_time()
