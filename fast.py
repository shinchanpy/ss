import asyncio
import os
import random
import sys
import time
import shutil
from playwright.async_api import async_playwright


RESET = "\033[0m"
RED = "\033[1;91m"
GREEN = "\033[1;92m"
YELLOW = "\033[1;93m"
BLUE = "\033[1;94m"
MAGENTA = "\033[1;95m"
CYAN = "\033[1;96m"
WHITE = "\033[1;97m"
ORANGE = "\033[38;5;208m"

# ================= DEFAULT CONFIGURATION =================
DEFAULT_SID = ["SESSION_ID"]
DEFAULT_URL = "GROUP_URL"
DEFAULT_OPPONENT = "HATTER_NAME"
DEFAULT_ENGINE_COUNT = 4
DELAY = 0.4
# =========================================================

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def professional_banner():
    clear()
    banner = f"""
    \033[1;31m --------------------------------------------
    \033[1;33m DEVELOPER : @vishaldied | @shinchanplugs
    \033[1;36m TOOL    : FAST SPAMMING
    \033[1;31m --------------------------------------------
    \033[0m"""
    print(banner)


STRIKE_MESSAGES = [
    "[{target}] - 𝗥𝗨𝗡𝗗𝗬 𝗞𝗔 𝗕𝗔𝗔𝗖𝗛𝗔 _________   🤣 𓂃\n\n",
    "[{target}] - 𝗥𝗨𝗡𝗗𝗬 𝗞𝗔 𝗕𝗔𝗔𝗖𝗛𝗔 _________   😂 𓂃\n\n",
    "[{target}] - 𝗥𝗨𝗡𝗗𝗬 𝗞𝗔 𝗕𝗔𝗔𝗖𝗛𝗔 _________   🤮 𓂃\n\n",
    "[{target}] - 𝗥𝗨𝗡𝗗𝗬 𝗞𝗔 𝗕𝗔𝗔𝗖𝗛𝗔 _________   🤑 𓂃\n\n",
    "[{target}] - 𝗥𝗨𝗡𝗗𝗬 𝗞𝗔 𝗕𝗔𝗔𝗖𝗛𝗔 _________   🤢 𓂃\n\n",
    "[{target}] - 𝗥𝗨𝗡𝗗𝗬 𝗞𝗔 𝗕𝗔𝗔𝗖𝗛𝗔 _________   🥵  𓂃\n\n",

]

def countdown(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r\033[1;32m    Starting Spam in {i} SECONDS... \033[0m")
        sys.stdout.flush()
        time.sleep(1)
    print("\n")

def get_payload(opponent):
    gap_lines = "\n" * 1  
    core = random.choice(STRIKE_MESSAGES).replace("{target}", opponent)
    return gap_lines.join([core] * 15) + "\n"

async def block_media(route):
    if route.request.resource_type in ["image", "media", "font"]:
        await route.abort()
    else:
        await route.continue_()

async def force_name_lock(page, gc_name):
    try:
        gear = page.locator('svg[aria-label="Conversation information"]')
        await gear.click()
        change_btn = page.locator('div[aria-label="Change group name"][role="button"]')
        group_input = page.locator('input[aria-label="Group name"][name="change-group-name"]')
        save_btn = page.locator('div[role="button"]:has-text("Save")')
        await change_btn.click()
        await group_input.fill(gc_name)
        if await save_btn.is_enabled():
            await save_btn.click()
            print(f"\033[1;32m    Name changed to : {gc_name}\033[0m")
        await gear.click()
    except Exception as e:
        print(f"    ⚠️ Error : {e}")
        await page.reload()

async def run_engine(engine_id, sid, url, opponent, gc_name, is_locker):
    user_data_dir = f"./session_data_{engine_id}"
    while True:
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir, headless=True,
                args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
            )
            await browser.add_cookies([{"name": "sessionid", "value": sid, "domain": ".instagram.com", "path": "/", "secure": True, "httpOnly": True}])
            page = await browser.new_page()
            await page.route("**/*", block_media)
            try:
                await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                msg_box = page.locator('div[role="textbox"], div[aria-label="Message"]').first
                
                msg_count = 0
                for _ in range(150): 
                    if msg_count > 0 and msg_count % 30 == 0:
                        print(f"    \033[1;33m Reloding tab : {engine_id}\033[0m")
                        await page.reload(wait_until='domcontentloaded')
                        msg_box = page.locator('div[role="textbox"], div[aria-label="Message"]').first
                        await msg_box.focus()

                    if is_locker and msg_count >= 19:
                        await force_name_lock(page, gc_name)
                        msg_count = 0
                        await msg_box.focus()
                    
                    await msg_box.focus()

                    await msg_box.fill(get_payload(opponent)) 
                    await page.keyboard.press("Enter")
                    
                    msg_count += 1
                    print(f"    \033[1;37mTab : {engine_id} : Sent : {msg_count} : @vishaldied | @shinchanplugs \033[0m")
                    await asyncio.sleep(random.uniform(DELAY, DELAY + 0.1))
                    
            except Exception as e:
                print(f"     [E-{engine_id}] Reloding Tab: {e}")
            
            await browser.close()
            if os.path.exists(user_data_dir):
                shutil.rmtree(user_data_dir, ignore_errors=True)
            await asyncio.sleep(1)

async def main():
    professional_banner()
    choice = input("        → Default  ? (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        sids, url, opponent, engine_count = DEFAULT_SID, DEFAULT_URL, DEFAULT_OPPONENT, DEFAULT_ENGINE_COUNT
    else:
        multi = input("        → Multiple IDs ? (y/n): ").strip().lower()
        if multi in ['y', 'yes']:
            sids = [s.strip() for s in input("        → Sessions ( S1,S3): ").split(',')]
        else:
            sids = [input("        → Session ID: ").strip()]
        url = input("        → GC Link: ").strip()
        opponent = input("        → Opponent : ").strip()
        engine_count = int(input("        → Tabs : ").strip() or 4)

    gc_name = f"[{opponent}] की मां रंडी ---/---"
    professional_banner()
    countdown(5)
    
    tasks = [run_engine(i+1, sids[i % len(sids)], url, opponent, gc_name, i == 0) for i in range(engine_count)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\033[1;31m  Stopped .... \033[0m")
        sys.exit()
