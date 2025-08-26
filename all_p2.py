# ENV :  hr
import gradio as gr

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import random
from prompts import Prompt_improvment_by_artist


def generate_image_from_prompt(prompt,negative_prompt, library, model_id='Anime', output_path='./image.png'):
    combined_prompt = f"{prompt} {library}"
    if model_id == 'Anime':
        model_name = 'dreamlike-art/dreamlike-anime-1.0'
    elif model_id == 'Fantasy':
        model_name = 'digiplay/Colorful_v3.1'
    elif model_id == 'Dream':
        model_name = 'Lykon/DreamShaper'
    elif model_id == 'Realistic':
        model_name = 'dreamlike-art/dreamlike-photoreal-2.0'
    elif model_id == 'Ink paint':
        model_name = 'Envvi/Inkpunk-Diffusion'
    elif model_id == 'Items':
        model_name = 'proximasanfinetuning/fantassified_icons_v2'
    
        
    pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    
    
    image = pipe(
        combined_prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=30,
        num_images_per_prompt=1,
        ).images[0] 
    image.save(output_path)
    return image, combined_prompt


def sentence_builder(model_id, Generate_prompt, Prompt, negative_prompt):
    print('len(model_id)',len(model_id))
    print('len(place)',len(Generate_prompt))
    print('len(Prompt)',len(Prompt))
    print('len(negative_prompt)',len(negative_prompt))
    # print('len(logo)',len(logo))
    
       
    if Generate_prompt=="Prompt_improvment_by_artist":
        Generate_prompt = random.choice(Prompt_improvment_by_artist)
    # elif Generate_prompt =="Random_prompt":
    #     Generate_prompt = random.choice(Random_prompt)
    # elif Generate_prompt =="Prompt_improvment_by_artist":
    #     Generate_prompt = random.choice(Prompt_improvment_by_artist)
    # elif Generate_prompt =="logo":
    #     Generate_prompt = random.choice(logo)
    output_prompt = f"{Prompt} {Generate_prompt} "
    
    # b    output_prompt = f"""The {quantity} {animal}s from {" and ".join(countries)} went to the {place} where they {" and ".join(activity_list)} until the {"morning" if morning else "night"}"""
    print('\n\n|-------- ',output_prompt)
    image, combined_prompt=generate_image_from_prompt(output_prompt, negative_prompt,library='', model_id=model_id)
    return combined_prompt, image


demo = gr.Interface(
    sentence_builder,
    [
        gr.Radio(["Anime", "Fantasy"], label="Style", info="Which style do you prefer?"),
        gr.Radio(["Prompt_improvment_by_artist"],label="Generate prompt", info=" "),
        gr.Text(label=" Select example prompts to generated images "),
        gr.Text(label="Negative prompt")
    ],
    ['text',
     "image"],
    
)


if __name__ == "__main__":
    demo.launch(share=True)



