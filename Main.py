from tkinter import*
from ttkthemes import ThemedTk
from tkinter import ttk
import openai
import requests
import os
import base64
from PIL import Image, ImageTk
OUTPUT_DIR = "outputs"
client = openai.OpenAI(api_key = "***ENTER YOUR OWN KEY***")
window=ThemedTk(theme="equilux")
window.title("PolyGenix")
window.geometry("550x450")
def download_image(url,filepath):
    img_data=requests.get(url).content
    with open(filepath,"wb") as f:
        f.write(img_data)
def generate_ideas(user_txt,n):
    prompt=(
    f"Generate {n} unique, creative ideas for a 3D printable model based on: {user_txt}\n"
    f"Return only a numbered list from 1 to {n}. One idea per line"
    )
    resp=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0.9,
    )
    ideas=[]
    for line in resp.choices[0].message.content.splitlines():
        print(line)
        line=line.strip()
        if line!="":
            ideas.append(line)
    return ideas[:n]
def process():
    global image_paths
    user=txt.get().strip()
    if rb.get()=="Choice1":
        n=1
    else:
        n=2
    ideas=generate_ideas(user,n)
    image_paths=generate_images_from_ideas2(ideas)
    cIndex=0
    showImage(0)
def showImage(ind):
    global imagePreview, image_label, image_paths
    img=Image.open(image_paths[ind])
    img=img.resize((400,400),Image.Resampling.LANCZOS)
    imagePreview=ImageTk.PhotoImage(img)
    image_label.config(image=imagePreview)

def nextImg(event=None):
    global cIndex
    if not image_paths:
        return
    cIndex = (cIndex+1)% len(image_paths)
    showImage(cIndex)

def prevImg(event=None):
    global cIndex
    if not image_paths:
        return
    cIndex = (cIndex - 1) % len(image_paths)
    showImage(cIndex)

def preview_first():
    global cIndex

    
def generate_images_from_ideas(ideas):
    paths=[]
    for i in range(len(ideas)):
        idea=ideas[i]
        img=client.images.generate(
            model="dall-e-3",
            prompt=idea,
            size="1024x1024",
            n=1
        )
        url=img.data[0].url
        print(url)
        filepath=OUTPUT_DIR+"/request_"+str(i+1)+".jpg"
        download_image(url,filepath)
        paths.append(filepath)
    return paths
def generate_images_from_ideas2(ideas):
    paths=[]

    for i in range(len(ideas)):
        img=client.images.generate(
            model="gpt-image-1.5",
            prompt=ideas[i],
            size="1024x1024",
            n=1,
            output_format="jpeg",
        )

        filepath=os.path.join(OUTPUT_DIR,f"request{i+1}.jpg")
        b64=img.data[0].b64_json
        print(b64)
        with open(filepath,"wb") as f:
            f.write(base64.b64decode(b64))
        paths.append(filepath)
    return paths

lbl=Label(window,text="PolyGenix")
lbl.place(x=240,y=50)
lbl0=Label(window,text="Idea Generation Engine for 3D Printable Designs")
lbl0.place(x=110,y=80)
rb = StringVar(value="Choice5")
rad1 = ttk.Radiobutton(window, text="Short [5 variants]", value="Choice1", variable=rb)
rad1.place(x=110, y=135)

rad2 = ttk.Radiobutton(window, text="Extended [15 Variants]", value="Choice2", variable=rb)
rad2.place(x=260, y=135)
txt=Entry(window)
txt.place(x=210, y=200)
btn=Button(window,text="Preview")
btn.place(x=180,y=230)
btn0=Button(window,text="Create",command=process)
btn0.place(x=300,y=230)
image_label=Label(window)
image_label.place(x=110, y=260)

window.mainloop()