import random
from openai import OpenAI
import time

class StoryGenerator:

    _location = ""
    _character = ""
    _beloved = ""
    _problem = ""
    _loveObstacle = ""
    _complication = ""
    _predicament = ""
    _crisis = ""
    _climax = ""

    plot_points = [
        _location,
        _character,
        _beloved,
        _problem,
        _loveObstacle,
        _complication,
        _predicament,
        _crisis,
        _climax,
        ]

    def __init__(self):
        #NOTE: You must use my personal API key to utilize our fine tuned GPT MODELS

        OPENAI_KEY = "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"

        PLOT_POINT_STORY_GENERATORID = "asst_Q9QWPefVFjzLUJtVzd8zxEW5" #This assistant takes plot points from plot genie in its story generator
        VANILLA_STORY_GENERATORID = "asst_o4BVrY2Bfpmp6A0oLPHG1tlO" #This assistant creates its own story from scratch


        self.openai_client = OpenAI(api_key=OPENAI_KEY)
        self.plot_point_assistant = self.openai_client.beta.assistants.retrieve(PLOT_POINT_STORY_GENERATORID)
        self.story_assistant = self.openai_client.beta.assistants.retrieve(VANILLA_STORY_GENERATORID)

    def get_story(self):
        self._get_plot_points()
        return(self.retrieve_AI_story)

    def retrieve_AI_story(self):
        prompt = ""
        options = [0,1,2,3,4,5,6,7,8]
        #story_num = random.randint(0,8)
        story_num = 2

        file_paths = ["Locations.txt",
              "Characters.txt",
              "Beloveds.txt",
              "Problems.txt",
              "LoveObstacles.txt",
              "Complications.txt",
              "Predicaments.txt",
              "Crisis.txt",
              "Climax.txt"]

        if story_num == 0:
            return self.__clean_output(self.__retrieve_message_from_openai(user_prompt=prompt, is_plot_point_assistant=False), story_num)

        else:
            for i in range(story_num):
                rand_story = random.choice(options)
                options.remove(rand_story)
                prompt += file_paths[rand_story].removesuffix(".txt") + ": " + self.plot_points[rand_story] + "."
                print(self.plot_points[rand_story])
            print(prompt)
            return self.__clean_output(self.__retrieve_message_from_openai(user_prompt=prompt, is_plot_point_assistant=True)), story_num


    def __clean_output(self, messages):
        final_message = messages.data[0].content[0].text.value

        final_message = final_message.replace('```', "")
        final_message = final_message.replace("json", "")

        return final_message


    def get_plot_points(self):
        file_paths = ["Locations.txt",
                      "Characters.txt",
                      "Beloveds.txt",
                      "Problems.txt",
                      "LoveObstacles.txt",
                      "Complications.txt",
                      "Predicaments.txt",
                      "Crisis.txt",
                      "Climax.txt"]
        names = []
        for file in file_paths:
            names.append(file.removesuffix(".txt"))

        categories = {name:[] for name in names}


        count = 0

        for file in file_paths:
            current_array = file.removesuffix(".txt")
            with open(file, 'r') as file:

                for line in file:
                    # Strip the newline character from the end of each line and add to the list
                    categories[current_array].append(line.strip())

            plot_num = random.randint(0,len(categories[current_array]))
            self.plot_points[count] = categories[current_array][plot_num]

            count += 1

        return self.plot_points

    def __retrieve_message_from_openai(self, user_prompt: str, is_plot_point_assistant: bool):
        thread = self.openai_client.beta.threads.create()

        message = self.openai_client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_prompt
        )

        if is_plot_point_assistant:
            run = self.openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.plot_point_assistant.id
            )
        else:
            run = self.openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.story_assistant.id
            )

        while True:
            time.sleep(5)

            run_status = self.openai_client.beta.threads.runs.retrieve(
                thread_id= thread.id,
                run_id= run.id
            )

            if run_status.status == "completed":
                print("Run is Completed")
                messages = self.openai_client.beta.threads.messages.list(
                thread_id=thread.id
                )
                break
            else:
                print("Run is in progress - Please Wait")
                continue

        return messages
