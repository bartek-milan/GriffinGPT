GriffinGPT
=============
A fully automated Python tool that generates Peter Griffin AI voice from long text — no character limits, no manual clicking, and automatic MP3 merging.

This script:
- Splits long text into clean, natural-sounding chunks
- Drives a browser automatically
- Downloads each generated MP3 piece
- Merges them into one final clean output file
- Cleans up temporary files
- Saves results as downloads/outputs/<first_two_words>_output.mp3
- Works totally hands-off
- Starts Chrome minimized so your desktop isn’t held hostage

Perfect for memes, narrations, YouTube intros, cursed projects, and anything that needs the voice of the man, the myth, the spherical unit himself.

-------------------------------------------------------------
How It Works
-------------------------------------------------------------
1. You give it text
2. The script slices it into readable voice chunks
3. Selenium opens the voice generator page
4. It pastes, clicks, waits, and downloads the audio
5. Everything is merged cleanly
6. The final MP3 goes into downloads/outputs/

-------------------------------------------------------------
Installation
-------------------------------------------------------------
Requirements:
- Python 3.10+
- Google Chrome installed
- ChromeDriver (auto-installed)

1. Clone the repository
    git clone https://github.com/bartek-milan/GriffinGPT.git
    cd GriffinGPT

2. Install required Python packages
    pip install -r requirements.txt

3. Run the script
    python main.py

Run with text file:
    python main.py mytext.txt

Run with inline text:
    python main.py "this is what peter griffin will say"

-------------------------------------------------------------
Output
-------------------------------------------------------------
Final generated MP3s are saved in:

    downloads/outputs/

File naming format:
    <first_two_words>_output.mp3

Example:
    massive_cylinder_output.mp3

-------------------------------------------------------------
Known Limitations
-------------------------------------------------------------
- If the AI voice site changes layout, the bot may freak out
- Requires active internet
- Chrome must be installed

-------------------------------------------------------------
License
-------------------------------------------------------------
Do whatever you want with it.  

-------------------------------------------------------------

Contributing
-------------------------------------------------------------
PRs welcome — new voices, better chunking, GUI additions, retries, everything.
TODO: closing the pop-up ads.

-------------------------------------------------------------
Stars
-------------------------------------------------------------
If this saved you hours of clicking and brainrot, consider starring the repo.  
It helps more people find it.
