import openai
import config
import gpt_config
import prompt

def gen_gs_query(description, words=0):
    openai.api_key = config.openai_api_key
    res = openai.ChatCompletion.create(
        model=gpt_config.gen_query_model,
        messages=prompt.gs_query_prompt(description)
    )
    ans = res['choices'][0]['message']['content']
    print(ans)
    return ans




def unit_test():
    des = "This paper presents a novel approach to auto sound synthesis in AR by leveraging 3D reconstraction, material recognition, and sound simulation techniques. Our method begins by scanning the target object and performing 3D reconstruction to capture its geometry. Next, we employ machine learning models to identify the object's physical materials, which play a crucial role in sound production. Once the object's geometry and material properties are obtained, we apply a sound simulation algorithm to generate realistic sound effects according to the object's material, geometry, and tapping location. As a result, our approcah allows users to interact with virtual objects in AR, producing sound effects that closely resemble those of their real-worl counterparts. This innovative method enhances user immersion and interaction within AR environments, paving the way for more realistic and engaging applications across various domains, including entertainment, education, and training."
    gen_gs_query(des)


if __name__ == "__main__":
    unit_test()
