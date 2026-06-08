import sys
import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright


async def check_ozon_position(query: str, target_sku: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        search_url = f"https://ozon.ru{query.replace(' ', '+')}&from_global=true"

        try:
            await page.goto(search_url, wait_until="load", timeout=30000)
            await page.wait_for_timeout(3000)

            links = await page.locator("a[href*='/product/']").all_links()

            found_position = "not_found"
            found_page = 1
            checked_count = 0
            unique_skus = []

            for link in links:
                href = link
                if "/product/" in href:
                    parts = href.split("/product/")[-1].split("/")
                    sku_candidate = parts[0].split("?")[0].strip("-").split("-")[-1]

                    if sku_candidate.isdigit() and sku_candidate not in unique_skus:
                        unique_skus.append(sku_candidate)
                        checked_count += 1

                        if sku_candidate == target_sku:
                            found_position = checked_count
                            break

                        if checked_count >= 100:
                            break

            total_checked = min(checked_count, 100)

            output = {
                "query": query,
                "sku": target_sku,
                "position": found_position,
                "page": found_page if found_position != "not_found" else 1,
                "total_checked": total_checked,
                "timestamp": datetime.now().isoformat()
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))

        except Exception as e:
            error_output = {
                "query": query,
                "sku": target_sku,
                "position": "not_found",
                "page": 1,
                "total_checked": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            print(json.dumps(error_output, ensure_ascii=False, indent=2))
        finally:
            await browser.close()


if __name__ == "__main__":
    test_query = sys.argv[1] if len(sys.argv) > 1 else "дождевик"
    test_sku = sys.argv[2] if len(sys.argv) > 2 else "4367148108"
    asyncio.run(check_ozon_position(test_query, test_sku))
