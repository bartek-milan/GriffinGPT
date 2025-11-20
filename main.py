from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pydub import AudioSegment
import base64
import time
import os
import sys
import traceback
import shutil


# ======= KONFIG henger =======
OLDAL = "https://theaivoicegenerator.com/peter-griffin-ai-voice/"
MAX_HOSSZ = 100
LETOLT_MAPP = os.path.join(os.getcwd(), "downloads")
OUTPUT_DIR = os.path.join(LETOLT_MAPP, "outputs")

os.makedirs(LETOLT_MAPP, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
# =============================


def darabokra_szaggalas(szoveg, max_len=MAX_HOSSZ):
    darabok = []
    mostani = ""

    break_jelek = {'.', ',', ';', ':', '!', '?'}

    for szo in szoveg.split():
        if mostani and len(mostani) + 1 + len(szo) > max_len:

            vagohely = -1
            for i in range(len(mostani) - 1, -1, -1):
                if mostani[i] in break_jelek:
                    vagohely = i + 1
                    break

            if vagohely != -1 and vagohely > 20:
                egy = mostani[:vagohely].strip()
                darabok.append(egy)
                mostani = mostani[vagohely:].strip() + " "
            else:
                darabok.append(mostani.strip())
                mostani = ""

        mostani += szo + " "

    if mostani.strip():
        darabok.append(mostani.strip())

    return darabok


def bongeszot_beallit():
    opciok = webdriver.ChromeOptions()
    opciok.add_argument("--disable-infobars")
    opciok.add_argument("--disable-extensions")
    opciok.add_argument("--start-minimized")
    opciok.add_argument("--window-position=2000,2000")  # moves window off-screen slightly

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opciok
    )
    return driver


def sutik_elfogad(driver):
    try:
        time.sleep(1)
        szel = [
            "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept')]",
            "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'agree')]",
            "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'consent')]",
            "//button[contains(@id,'accept')]",
            "//button[contains(@id,'agree')]",
            "//button[contains(@class,'accept')]",
            "//button[contains(@class,'agree')]",
            "//button[contains(@class,'consent')]",
        ]

        for x in szel:
            gombok = driver.find_elements(By.XPATH, x)
            for g in gombok:
                if g.is_displayed() and g.is_enabled():
                    driver.execute_script("arguments[0].click();", g)
                    print("Cookies accepted")
                    return
    except:
        pass


def audio_link_kereso(driver):
    try:
        aelemek = driver.find_elements(
            By.XPATH, "//a[contains(@class,'fmtts-btn-secondary') and @href]"
        )
        for a in aelemek:
            href = a.get_attribute("href") or ""
            if href.startswith("data:audio"):
                return a
    except:
        pass
    return None


def varakozas_audio(driver, timeout=60):
    w = WebDriverWait(driver, timeout)
    try:
        return w.until(lambda d: audio_link_kereso(d))
    except:
        return None


def peter_hang_lecsinal(darabok):
    bongi = bongeszot_beallit()
    var = WebDriverWait(bongi, 30)

    try:
        bongi.get(OLDAL)
        sutik_elfogad(bongi)
        time.sleep(2)

        for i, darab in enumerate(darabok):
            print(f"\n--- Processing part {i+1}/{len(darabok)} ---")
            print(darab)

            if i > 0:
                print("Refreshing page...")
                bongi.get(OLDAL)
                time.sleep(2)
                sutik_elfogad(bongi)
                time.sleep(1)

            if i == 1:
                print("Adding 1 second delay...")
                time.sleep(1)

            textdoboz = var.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            if not textdoboz.is_displayed():
                for ta in bongi.find_elements(By.TAG_NAME, "textarea"):
                    if ta.is_displayed():
                        textdoboz = ta
                        break

            try:
                textdoboz.clear()
            except:
                bongi.execute_script("arguments[0].value = '';", textdoboz)

            textdoboz.send_keys(darab)
            time.sleep(0.3)

            gen_gomb = None
            xpathok = [
                "//button[contains(., 'Generate Voice')]",
                "//button[contains(., 'Generate')]",
                "//button[contains(@class,'fmtts-btn-primary')]",
                "//button[.//span[contains(., 'Generate')]]"
            ]

            for xp in xpathok:
                try:
                    b = bongi.find_element(By.XPATH, xp)
                    if b.is_displayed() and b.is_enabled():
                        gen_gomb = b
                        break
                except:
                    pass

            if not gen_gomb:
                print("Generate button not found")
                continue

            bongi.execute_script("arguments[0].scrollIntoView({behavior:'instant',block:'center'});", gen_gomb)

            try:
                gen_gomb.click()
            except:
                bongi.execute_script("arguments[0].click();", gen_gomb)

            print("Waiting for audio...")
            link = varakozas_audio(bongi)

            if not link:
                print("Audio failed")
                continue

            href = link.get_attribute("href")
            if not href.startswith("data:audio"):
                print("Invalid audio link:", href[:60])
                continue

            b64 = href.split("base64,", 1)[1]
            bajt = base64.b64decode(b64)

            ut = os.path.join(LETOLT_MAPP, f"resz_{i+1}.mp3")
            with open(ut, "wb") as f:
                f.write(bajt)

            print("Saved:", ut)
            time.sleep(1)

    except Exception:
        print("ERROR:\n", traceback.format_exc())
    finally:
        try:
            bongi.quit()
        except:
            pass


def teljes_letakaritas():
    for f in os.listdir(LETOLT_MAPP):
        ut = os.path.join(LETOLT_MAPP, f)
        if os.path.isfile(ut) and f.lower().endswith(".mp3"):
            try:
                os.remove(ut)
            except:
                pass


def osszefuzes(darabok):
    fajlok = [
        f for f in os.listdir(LETOLT_MAPP)
        if f.lower().endswith(".mp3")
    ]

    if not fajlok:
        print("Nothing to merge")
        return

    def kulcs(fn):
        try:
            return int(fn.split("_")[1].split(".")[0])
        except:
            return 9999

    fajlok = sorted(fajlok, key=kulcs)

    elso = darabok[0].split()
    if len(elso) >= 2:
        prefix = f"{elso[0]}_{elso[1]}"
    elif len(elso) == 1:
        prefix = elso[0]
    else:
        prefix = "output"

    prefix = "".join(c for c in prefix if c.isalnum() or c == "_")
    cel_nev = prefix + "_output.mp3"
    cel_ut = os.path.join(OUTPUT_DIR, cel_nev)

    kombo = AudioSegment.empty()
    for fn in fajlok:
        kombo += AudioSegment.from_mp3(os.path.join(LETOLT_MAPP, fn))

    kombo.export(cel_ut, format="mp3")
    print("Merged final file:", cel_ut)

    for fn in fajlok:
        try:
            os.remove(os.path.join(LETOLT_MAPP, fn))
        except:
            pass


# ======== MAIN =========
if __name__ == "__main__":
    szoveg = input("what would you like Peter to say? e.g Massive Cylinder \n")

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.exists(arg):
            szoveg = open(arg, "r", encoding="utf8").read()
        else:
            szoveg = " ".join(sys.argv[1:])

    darabok = darabokra_szaggalas(szoveg)
    print("Parts:", len(darabok))

    teljes_letakaritas()

    peter_hang_lecsinal(darabok)
    osszefuzes(darabok)

    teljes_letakaritas()
