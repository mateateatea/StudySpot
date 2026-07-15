from playwright.sync_api import Page, expect

def test_successful_ui_reservation(page: Page):
    page.goto("http://127.0.0.1:8000")

    page.locator("#placeId").select_option("3")

    page.locator("#date").fill("2026-07-25")
    page.locator("#timeSlot").fill("12:00")

    page.locator("#reserveBtn").click()

    message_box = page.locator("#message")
    expect(message_box).to_contain_text("successfully reserved")

def test_cannot_book_same_slot_twice(page: Page):
    page.goto("http://127.0.0.1:8000")

    page.locator("#placeId").select_option("4")
    page.locator("#date").fill("2026-07-15")
    page.locator("#timeSlot").fill("14:00")

    page.locator("#reserveBtn").click()

    message_box = page.locator("#message")
    expect(message_box).to_contain_text("already booked")