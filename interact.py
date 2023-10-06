import time
import argparse
import torch
import msgpack
from drqa.model import DocReaderModel
from drqa.utils import str2bool
from prepro import annotate, to_id, init
from train import BatchGen
import discord
from discord.ext.commands import Cog, command


class Interact(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_interact(self, message, st):
        parser = argparse.ArgumentParser(                                                                                                                                               
            description='Interact with document reader model.'                                                                                                                                       
        )
        parser.add_argument('--model-file', default='models/best_model.pt',
                            help='path to model file')
        parser.add_argument("--cuda", type=str2bool, nargs='?',
                            const=True, default=torch.cuda.is_available(),
                            help='whether to use GPU acceleration.')
        args = parser.parse_args()

        if args.cuda:
            checkpoint = torch.load(args.model_file)
        else:
            checkpoint = torch.load(
                args.model_file, map_location=lambda storage, loc: storage)

        state_dict = checkpoint['state_dict']
        opt = checkpoint['config']
        with open('SQuAD/meta.msgpack', 'rb') as f:
            meta = msgpack.load(f)
        embedding = torch.Tensor(meta['embedding'])
        opt['pretrained_words'] = True
        opt['vocab_size'] = embedding.size(0)
        opt['embedding_dim'] = embedding.size(1)
        opt['pos_size'] = len(meta['vocab_tag'])
        opt['ner_size'] = len(meta['vocab_ent'])
        opt['cuda'] = args.cuda
        BatchGen.pos_size = opt['pos_size']
        BatchGen.ner_size = opt['ner_size']
        model = DocReaderModel(opt, embedding, state_dict)
        w2id = {w: i for i, w in enumerate(meta['vocab'])}
        tag2id = {w: i for i, w in enumerate(meta['vocab_tag'])}
        ent2id = {w: i for i, w in enumerate(meta['vocab_ent'])}
        init()

        id_ = 0
        try:
            while True:
                evidence = ("Gamification describes the use of game design elements in different contexts. This includes the creation of learning experiences that use challenges, rewards, points, points and others, in the framework of the objectives of the game.The application of gamification in learning contexts allows the use of games as educational tools. This approach aims to increase the student's knowledge through the game, either in a formal or informal educational context. In fact, game design components and patterns intrinsically contain some form of learning in the mechanics itself.The objective of this work is to increase the time and effort that students dedicate to learning. It is essential that the student is involved in the learning process and that he/she has high levels of motivation. If he is motivated to learn, he spends more time and devotes more effort to learning, feeling, at the same time, better with what he learns. Even this pattern will be repeated throughout life, allowing you to maintain a positive attitude and constant self-improvement. This posture arises naturally when the student is involved in the learning experience, through intrinsically motivating activities.Given that the evaluation is transversal throughout the semester, it was decided to use a mechanics of achievements as a basis for the evaluation and classification model. In this way, it was possible to frame the chapters and learning experiences as contributions to the evaluation and classification. At the end of the semester, the summative evaluation resulted directly in the classification, without the performance of written examinations or additional papers.With the design of the evaluation and classification model completed, the learning experiences were developed taking into account that they should be diversified, integrating, appealing to the largest number of students and allowing each student to select the level of difficulty most appropriate to the successful progression of their learning.According to the Bologna principles, the skills to be acquired and the curriculum do not change. Learning experiences include traditional hands-on work, predicting situations where students don't like to play, and diverse games, all with educational content.The participation of students in all phases was encouraged, from the preparation and discussion of the new structure to the development of learning experiences, in order to acquire awareness of the changes and enhance participation.The GSR curriculum is structured, according to the UC form, into four sections or chapters. Each section covers several topics that support the knowledge to be acquired in the following sections. The final classification depends on the success in each section as well as the creativity and level of knowledge shown. Students are classified from 0 to 20 which, translating to the ECTS rating scale, demonstrate their relative performance (the best 10 per cent get grade A, the following 25 per cent get grade B, at 30 per cent grade C is awarded, at 25 per cent grade D and, at the last 10%, grade E). The student approves with a rating equal to or greater than 10 (0-20).The evaluation and rating system designed for GSR assumes the achievement structure of a game. All students must complete the minimum requirements to successfully complete UC. In other words, the student will have to go through all sections (or levels), which will award him a grade 10. In each level, the increasing number of obstacles overcome will allow the student to obtain a higher rating.Each level is represented by a castle on an island, which the student will have to conquer. Additionally, the student can also gather up to 2 stars, associated with the complexity of the obstacles overcome. When an obstacle is overcome, the student also receives BitPoints, used to buy tools and extra help to the teacher. In other words, the evaluation system consists of castles, stars and points.The level map also gives you access to the article store, where the student can purchase information or tools to be used in other tasks. The list of articles includes several articles that can be valuable to overcome some obstacles.The list of articles includes: a command line string (at 50 bitpoints), a virtual machine (at 250 bitpoints), a step-by-step configuration script (for 350 bitpoints), a configuration file (for 500 bitpoints), and finally the configured service (for 999 bitpoints).As described earlier, the student progresses by completing levels and collecting stars and BitPoints without any restriction. The number, size and complexity of each level is associated with the content planned for the corresponding chapter. In other words, the design of each level is indexed to the associated chapter in the GSR curriculum. However, to stimulate motivation, a fifth level is added.The levels are: virtualization and operating systems, isolated systems, networking systems, integrated network management and integration of concepts.The size of each level determines the complexity and number of learning experiences the student has to complete before moving on to the next. It also determines the time required.Stars are awarded according to the degree of difficulty that the student has chosen to complete the level. Each presents several practical works and games, giving you the possibility to choose according to the desired difficulty. Thus, the easy level represents the simplest, normal jobs and games, with jobs and games a little more complex and ultimately difficult, with the games and more difficult jobs.BitPoints are awarded whenever a learning experience is completed. This virtual currency is used by the student to buy tools and information that helps him in more complex challenges. In this context, the amount granted depends on the number and complexity of the learning experience, the time required to complete it and participation in the classes.The student can accumulate BitPoints in each learning experience. The more you complete, the more you get.The student has permanent access to the progress report in constantly updated PDF format. The report can be downloaded to the progress map by selecting the icon in the format of an old book in the lower left corner.The term learning experiences are not typically used to describe formal learning activities, such as transmissive methodologies in the classroom. Centered on the student, this term describes that he is experiencing something that contributes to a change in the way he thinks, perceives or acts.For this to be done, learning experiences must be active, meaningful, socially meaningful, integrative and diverse. These are considered active when the student assumes the main role of the learning process. They should provide knowledge and expertise that directly contribute to the student's ability to perform the learning process more effectively. Sharing and cooperation is essential, allowing the student to interact with colleagues.The constant increase in complexity requires the integration of various dimensions of knowledge, easier to acquire when experiences are diverse. In this context, teaching and learning go beyond the acquisition of traditional knowledge, representing a do-think-how learning process.Learning experiences should be appropriate to motivate students and provide the necessary challenges for learning to succeed. In this context, the concept is assumed as a reinforcement to educational interaction regarding its location (school, classroom) or format (curricular unit, course).The diversity of ways in which the student builds his knowledge and interacts with teachers, associated with the difference in the level of independence and autonomy of each one, is considerable. In order to be as comprehensive as possible, learning experiences were designed to include traditional practical work, design and game play. The latter are an integral part of the construction of knowledge, so they have the objective of being educational focusing mainly on the cognitive aspect of learning.According to the UC form, the structure was designed on five levels, with three degrees of difficulty in each of them, allowing the organizing of learning experiences in stages of increasing complexity.Each degree of difficulty at each level is implemented in specific learning experiences. The student can choose at least one easy, normal or difficult challenge that they will have to complete in order to successfully achieve the level.According to the GSR curriculum, the student uses virtual machines and operating systems installation to implement various exercises. It has to carry out practical work in order to install, configure and test the techniques and mechanisms of the program. The practical work is complemented with theoretical concepts, explaining the role, protocols and architectures of the systems to be implemented.Each TP is accompanied by a report, to be evaluated by the teacher. These are not evaluated with a rating. The report will be either accepted or rejected, in which case the student may, if desired, modify and improve and resubmit the evaluation. Only when the report is accepted, will the work be considered as successfully completed.The Virtualization Game consists of a Card Game, to be played by 3 to 5 players around a table. It uses cards as the primary support device. There are many and varied types and styles of card games, from those played with traditional cards to those that use cards designed specifically for certain games.The overall goal for this game is to allow students to describe a set of virtualization tools and concepts. This is translated into the following learning objectives: to sum up the main concepts of virtualization; classify the virtualization components; identify advantages and drawbacks of virtualization.According to previous learning objectives, the student has to apply a research-development-use cycle to develop a card game that allows him to use concepts, information and facts about virtualization.The process of drawing the letters requires students to investigate and then sumatify the information in a set of letters. The cards are then drawn and grouped into a deck.The deck of cards is used to practice sorting concepts about virtualization. This step is done in a group of students, during classes, according to a set of defined rules.The cards are distinguished by the graphic appearance. Students are free to create their theme or appearance. The back does not contain information to reveal the front. The front part should allow you to distinguish VM Cards from Incident Cards, which can be in the form of an image, graphic, question, instructions, or others.Dred City is an RPG-type game, framed in the second level.  Each participant assumes the role of a character, usually in a fantasy or science fiction framework, and interacts with the imaginary world of the game. Players are responsible for playing a role within a narrative, following a character development or decision-making process.")
                if evidence.strip():
                    break
            while True:
                question = st
                if question.strip():
                    break
        except EOFError:
            print()

        id_ += 1
        start_time = time.time()
        annotated = annotate(
            ('interact-{}'.format(id_), evidence, question), meta['wv_cased'])
        model_in = to_id(annotated, w2id, tag2id, ent2id)
        model_in = next(
            iter(BatchGen([model_in], batch_size=1, gpu=args.cuda, evaluation=True)))
        prediction = model.predict(model_in)[0]
        end_time = time.time()
        await message.author.send('{}'.format(prediction))
        print('Answer: {}'.format(prediction))
        print('Time: {:.4f}s'.format(end_time - start_time))
