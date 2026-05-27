import asyncio
import os
import random
import time
from pathlib import Path
from playwright.async_api import async_playwright,expect
import re
# =========================
# CONFIG
# =========================

BASE_URL = "https://iqp.fngt.pro"
USERNAME = "hungnx22@example.com"
PASSWORD = "F2am4wV533001"

GRAPH_NAME = "a1"

DOCS_FOLDER = "./docs"

CONCURRENT_USERS = 1

HEADLESS = False

# =========================
# HELPERS
# =========================

def get_documents(num_random=None):
    docs_path = Path(DOCS_FOLDER)

    if not docs_path.exists():
        raise Exception(f"Docs folder not found: {DOCS_FOLDER}")

    files = [
        str(file)
        for file in docs_path.iterdir()
        if file.is_file()
    ]

    if not files:
        raise Exception("No files found inside docs folder")

    if num_random is not None:
        if num_random > len(files):
            raise Exception(f"Cannot select {num_random} random documents. Only {len(files)} available")
        return random.sample(files, num_random)

    return files


async def login(page):
    await page.goto("https://iqp.fngt.pro/login")

    # wait form visible
    await page.wait_for_selector('input[type="email"]')

    # email
    await page.fill(
        'input[type="email"]',
        USERNAME
    )

    # password
    await page.fill(
        'input[type="password"]',
        PASSWORD
    )

    # click sign in
    await page.click('button[type="submit"]')
    # add wait 1-2 sec before continue
    await page.wait_for_timeout(3000)
    # wait after login
    await page.wait_for_load_state("networkidle")

    print("Login successful")


async def run_ingestion(user_id, browser, documents):
    context = await browser.new_context()

    page = await context.new_page()

    start_time = time.time()

    try:
        print(f"[User {user_id}] Starting...")

        # =========================
        # LOGIN
        # =========================

        await login(page)

        print(f"[User {user_id}] Login success")

        # =========================
        # NAVIGATE TO INGESTION PAGE
        # =========================

        # update URL if needed
        print("go to ingestion page")
        await page.goto("https://iqp.fngt.pro/workspace/d5db5451-37ce-41c3-8296-df0c6f00c406/ingestion?graph_id=graph_20260526_080629_212987")

        await page.wait_for_load_state("networkidle")
        
        # verify we're on ingestion page
        current_url = page.url
        print(f"[User {user_id}] Current URL: {current_url}")
        
        # await page.pause()
        #### view all selector on current page
        
        # wait for file upload element to confirm page loaded
        # await page.wait_for_selector('input[type="unstructured-file-upload"]', timeout=15000)
        print(f"[User {user_id}] Ingestion page loaded successfully")

    
        # =========================
        # UPLOAD DOCUMENTS
        # =========================

        # 2. Định vị chính xác thẻ <input> ẩn bằng ID của nó
        file_input = page.locator('#unstructured-file-upload')

        # 3. Đảm bảo input đã được gắn vào DOM trước khi tương tác
        await file_input.wait_for(state="attached")

        # 4. Thực hiện upload danh sách file (Playwright tự xử lý được input bị ẩn)
        await file_input.set_input_files(documents)

        print(f"[User {user_id}] Uploaded {len(documents)} files")
        # =========================
        # CLICK INGEST BUTTON
        # =========================

        # update selector if needed
        await page.get_by_role("button", name="Analyze Configuration").click()


        # =========================
        # WAIT FOR COMPLETION
        # =========================

        # Wait for the analysis to complete
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector('button:has-text("Confirm & Ingest Graph")', timeout=60000)

        await page.get_by_role("button", name=" Confirm & Ingest Graph").click()

        # Wait for integration to complete (up to 5 minutes)
        await page.wait_for_selector(
            'text="Integration Complete! The Knowledge Graph semantic layer has been enriched."',
            timeout=300000
        )

        await page.get_by_role("button", name="View Graph Overview").click()


        await page.get_by_role("button", name=re.compile(r"^Commit")).click(force=True)

        await page.get_by_role("button", name="Commit", exact=True).click()

        await expect(page.get_by_role("button", name="Committing...")).to_have_count(0)

        # total_edge = page.locator("div.glass").filter(has_text="Total Edges")
        # edge_count = total_edge.locator("span[style*='tabular-nums']").inner_text()
        # total_node = page.locator("div.glass").filter(has_text="Total Nodes")
        # node_count = total_node.locator("span[style*='tabular-nums']").inner_text()

        # if edge_count > 0 and node_count > 0:
        #     print(f"[User {user_id}] Ingestion completed successfully with {node_count} nodes and {edge_count} edges")
        duration = round(time.time() - start_time, 2)

        print(
            f"[User {user_id}] SUCCESS "
            f"(Duration: {duration}s)"
        )

    except Exception as e:
        duration = round(time.time() - start_time, 2)

        print(
            f"[User {user_id}] FAILED "
            f"(Duration: {duration}s)"
        )

        print(f"[User {user_id}] Error: {e}")

        screenshot_path = f"screenshot_user_{user_id}.png"

        await page.screenshot(path=screenshot_path)

        print(
            f"[User {user_id}] Screenshot saved: "
            f"{screenshot_path}"
        )

    finally:
        await context.close()


async def main():
    documents = get_documents(1)

    print("=" * 60)
    print(f"Found {len(documents)} documents")
    print(f"Concurrent users: {CONCURRENT_USERS}")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=HEADLESS
        )

        tasks = []

        for user_id in range(1, CONCURRENT_USERS + 1):
            tasks.append(
                run_ingestion(
                    user_id,
                    browser,
                    documents
                )
            )

        start = time.time()

        await asyncio.gather(*tasks)

        total_duration = round(time.time() - start, 2)

        print("=" * 60)
        print("LOAD TEST FINISHED")
        print(f"Total duration: {total_duration}s")
        print("=" * 60)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
