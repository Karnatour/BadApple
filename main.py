from PIL import Image, ImageOps
import subprocess
import os
import winsound
import fpstimer
import shutil

# TODO Multi threading

ASCII_CHARS = [" ", ",", ";", "+", "*", "?", "#", "%"]


def main():
    createdir()
    userinput = input("1) Vlastní video\n"
                      "2) Default=BadApple\n"
                      "3) Přehrátí framů(Pouze pokud už jste je předtím stáhnuli)\n")
    if userinput == "1":
        download()
        resize()
        grayscale()
        convert_to_ascii()
        play_ascii()
    elif userinput == "2":
        default()
        resize()
        grayscale()
        convert_to_ascii()
        play_ascii()
    else:
        play_ascii()
    delete = input("\nPokud chcete smazat framy napiště '1'")
    if delete == "1":
        shutil.rmtree("temp", ignore_errors=True)
    else:
        return 0


def download():
    URL = input("Zadejte url adresu\n")
    # Stáhne MP4 soubor
    subprocess.run(["yt-dlp.exe", "-f best", "-o", "out.%(ext)s", URL])
    os.replace("out.mp4", "temp/out.mp4")
    # Převede MP4 soubor na wav
    print("Převádím MP4 soubor na wav\n")
    subprocess.run(["ffmpeg.exe", "-i", "temp/out.mp4", "temp/audio.wav"])
    # Převede MP4 soubor na 8 bit bmp framy
    print("Převádím MP4 soubor na bmp\n")
    subprocess.run(["ffmpeg.exe", "-i", "temp/out.mp4", "-pix_fmt", "bgr8", "temp/frames/frame%05d.bmp"])


def default():
    URL = "https://www.youtube.com/watch?v=FtutLA63Cp8&ab_channel=kasidid2"
    # Stáhne MP4 soubor
    subprocess.run(["yt-dlp.exe", "-f best", "-o", "out.%(ext)s", URL])
    os.replace("out.mp4", "temp/out.mp4")
    # Převede MP4 soubor na wav
    print("Převádím MP4 soubor na WAV\n")
    subprocess.run(["ffmpeg.exe", "-i", "temp/out.mp4", "temp/audio.wav"])
    # Převede MP4 soubor na 8 bit bmp framy
    print("Převádím MP4 soubor na bmp\n")
    subprocess.run(["ffmpeg.exe", "-i", "temp/out.mp4", "-pix_fmt", "bgr8", "temp/frames/frame%05d.bmp"])


def resize():
    print("Měním rozlišení")
    maxcount = len(os.listdir('temp/frames')) + 1
    count = 1
    global new_width
    new_width = 236
    while count != maxcount:
        img = Image.open("temp/frames/frame{:05d}.bmp".format(count))
        old_width, old_height = img.size
        ratio = old_height / old_width / 2.5
        new_height = int(new_width * ratio)
        new_img = img.resize((new_width, new_height))
        new_img.save("temp/resizedframes/frame{:05d}.bmp".format(count))
        count += 1


def grayscale():
    print("Aplikuji grayscale\n")
    maxcount = len(os.listdir('temp/resizedframes')) + 1
    count = 1
    while count != maxcount:
        old_img = Image.open("temp/resizedframes/frame{:05d}.bmp".format(count))
        img = ImageOps.grayscale(old_img)
        img.save("temp/grayscale/frame{:05d}.bmp".format(count))
        count += 1


def convert_to_ascii():
    print("Převádím bmp soubory na ASCII (Tohle může nějakou dobu trvat)")
    maxcount = len(os.listdir('temp/grayscale')) + 1
    count = 1
    while count != maxcount:
        old_img = Image.open("temp/grayscale/frame{:05d}.bmp".format(count))
        pixels = old_img.getdata()
        ascii_str = ""
        ascii_image = ""
        for pixel in pixels:
            ascii_str += ASCII_CHARS[pixel // 35]
        ascii_str_len = len(ascii_str)
        for i in range(0, ascii_str_len):
            ascii_image = "\n".join(ascii_str[i:(i + new_width)] for i in range(0, ascii_str_len, new_width))
        with open("temp/ascii/frame{:05d}.txt".format(count), "w", encoding="utf-8") as f:
            f.write(ascii_image)
        print("Progress: {} / {}\n".format(count, maxcount - 1), end="\r")
        count += 1


def play_ascii():
    maxcount = len(os.listdir('temp/ascii'))
    count = 1
    # interval = input("Zadejte časovou mezeru mezi framy (doporučená hodnota: 0.03)")
    winsound.PlaySound("temp/audio.wav", winsound.SND_ASYNC or winsound.SND_ALIAS)
    timer = fpstimer.FPSTimer(30)
    while count != maxcount:
        print(open("temp/ascii/frame{:05d}.txt".format(count)).read())
        count += 1
        timer.sleep()
    winsound.PlaySound(None, winsound.SND_ASYNC)


def createdir():
    try:
        os.mkdir("temp")
        os.mkdir("temp/frames")
        os.mkdir("temp/resizedframes")
        os.mkdir("temp/grayscale")
        os.mkdir("temp/ascii")
        print("Složka temp byla úspěšně vytvořena")
    except:
        print("Složka temp již existuje nepotřebuji ji vytvářet")


if __name__ == "__main__":
    main()
