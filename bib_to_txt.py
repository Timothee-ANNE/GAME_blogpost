"""
Format BibTeX entries as: label: Author(s), "Title," Venue, details, year.
Usage: python format_bib.py references.bib
       python format_bib.py  (reads from refs.bib in same dir)
"""

import re
import sys

BIB = """
@article{pugh2016quality,
  title={Quality diversity: A new frontier for evolutionary computation},
  author={Pugh, Justin K and Soros, Lisa B and Stanley, Kenneth O},
  journal={Frontiers in Robotics and AI},
  volume={3},
  pages={40},
  year={2016},
  publisher={Frontiers Media SA}
}

@inproceedings{gravina2019procedural,
  title={Procedural content generation through quality diversity},
  author={Gravina, Daniele and Khalifa, Ahmed and Liapis, Antonios and Togelius, Julian and Yannakakis, Georgios N},
  booktitle={2019 IEEE Conference on Games (CoG)},
  pages={1--8},
  year={2019},
  organization={IEEE}
}

@article{jiang2022artificial,
  title={An artificial intelligence enabled chemical synthesis robot for exploration and optimization of nanomaterials},
  author={Jiang, Yibin and Salley, Daniel and Sharma, Abhishek and Keenan, Graham and Mullin, Margaret and Cronin, Leroy},
  journal={Science advances},
  volume={8},
  number={40},
  pages={eabo2626},
  year={2022},
  publisher={American Association for the Advancement of Science}
}

@article{cully2015robots,
  title={Robots that can adapt like animals},
  author={Cully, Antoine and Clune, Jeff and Tarapore, Danesh and Mouret, Jean-Baptiste},
  journal={Nature},
  volume={521},
  number={7553},
  pages={503--507},
  year={2015},
  publisher={Nature Publishing Group UK London}
}

@book{schelling1980strategy,
  title={The Strategy of Conflict: with a new Preface by the Author},
  author={Schelling, Thomas C},
  year={1980},
  publisher={Harvard university press}
}

@book{baldwin2011understanding,
  title={Understanding regulation: theory, strategy, and practice},
  author={Baldwin, Robert and Cave, Martin and Lodge, Martin},
  year={2011},
  publisher={Oxford university press}
}

@article{chakraborty2018adversarial,
  title={Adversarial attacks and defences: A survey},
  author={Chakraborty, Anirban and Alam, Manaar and Dey, Vishal and Chattopadhyay, Anupam and Mukhopadhyay, Debdeep},
  journal={arXiv preprint arXiv:1810.00069},
  year={2018}
}

@article{li2021arms,
  title={Arms race in adversarial malware detection: A survey},
  author={Li, Deqiang and Li, Qianmu and Ye, Yanfang and Xu, Shouhuai},
  journal={ACM Computing Surveys (CSUR)},
  volume={55},
  number={1},
  pages={1--35},
  year={2021},
  publisher={ACM New York, NY}
}

@article{samvelyan2024multi,
  title={Multi-agent diagnostics for robustness via illuminated diversity},
  author={Samvelyan, Mikayel and Paglieri, Davide and Jiang, Minqi and Parker-Holder, Jack and Rocktaschel, Tim},
  journal={arXiv preprint arXiv:2401.13460},
  year={2024}
}

@article{zhang2023omni,
  title={Omni: Open-endedness via models of human notions of interestingness},
  author={Zhang, Jenny and Lehman, Joel and Stanley, Kenneth and Clune, Jeff},
  journal={arXiv preprint arXiv:2306.01711},
  year={2023}
}

@article{vinyals2019grandmaster,
  title={Grandmaster level in StarCraft II using multi-agent reinforcement learning},
  author={Vinyals, Oriol and Babuschkin, Igor and Czarnecki, Wojciech M and Mathieu, Micha{\"e}l and Dudzik, Andrew and Chung, Junyoung and Choi, David H and Powell, Richard and Ewalds, Timo and Georgiev, Petko and others},
  journal={nature},
  volume={575},
  number={7782},
  pages={350--354},
  year={2019},
  publisher={Nature Publishing Group}
}

@inproceedings{lehman2011evolving,
  title={Evolving a diversity of virtual creatures through novelty search and local competition},
  author={Lehman, Joel and Stanley, Kenneth O},
  booktitle={Proceedings of the 13th annual conference on Genetic and evolutionary computation},
  pages={211--218},
  year={2011}
}

@inproceedings{vassiliades2017comparison,
  title={A comparison of illumination algorithms in unbounded spaces},
  author={Vassiliades, Vassilis and Chatzilygeroudis, Konstantinos and Mouret, Jean-Baptiste},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference Companion},
  pages={1578--1581},
  year={2017}
}

@inproceedings{iovino2021learning,
  title={Learning behavior trees with genetic programming in unpredictable environments},
  author={Iovino, Matteo and Styrud, Jonathan and Falco, Pietro and Smith, Christian},
  booktitle={2021 IEEE International Conference on Robotics and Automation (ICRA)},
  pages={4591--4597},
  year={2021},
  organization={IEEE}
}

@article{stanley2002evolving,
  title={Evolving neural networks through augmenting topologies},
  author={Stanley, Kenneth O and Miikkulainen, Risto},
  journal={Evolutionary computation},
  volume={10},
  number={2},
  pages={99--127},
  year={2002},
  publisher={MIT Press}
}

@inproceedings{montague2023quality,
  title={A quality-diversity approach to evolving a repertoire of diverse behaviour-trees in robot swarms},
  author={Montague, Kirsty and Hart, Emma and Nitschke, Geoff and Paechter, Ben},
  booktitle={International Conference on the Applications of Evolutionary Computation},
  pages={145--160},
  year={2023},
  organization={Springer}
}

@book{colledanchise2018behavior,
  title={Behavior trees in robotics and AI: An introduction},
  author={Colledanchise, Michele and Ogren, Petter},
  year={2018},
  publisher={CRC Press}
}

@inproceedings{mouret2020quality,
  title={Quality diversity for multi-task optimization},
  author={Mouret, Jean-Baptiste and Maguire, Glenn},
  booktitle={Proceedings of the 2020 Genetic and Evolutionary Computation Conference},
  pages={121--129},
  year={2020}
}

@inproceedings{cully2019autonomous,
  title={Autonomous skill discovery with quality-diversity and unsupervised descriptors},
  author={Cully, Antoine},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference},
  pages={81--89},
  year={2019}
}

@article{vassiliades2016scaling,
  title={Scaling up map-elites using centroidal voronoi tessellations},
  author={Vassiliades, Vassilis and Chatzilygeroudis, Konstantinos and Mouret, Jean-Baptiste},
  journal={arXiv preprint arXiv:1610.05729},
  year={2016}
}

@inproceedings{radford2021learning,
  title={Learning transferable visual models from natural language supervision},
  author={Radford, Alec and Kim, Jong Wook and Hallacy, Chris and Ramesh, Aditya and Goh, Gabriel and Agarwal, Sandhini and Sastry, Girish and Askell, Amanda and Mishkin, Pamela and Clark, Jack and others},
  booktitle={International conference on machine learning},
  pages={8748--8763},
  year={2021},
  organization={PmLR}
}

@inproceedings{anne2023multi,
  title={Multi-task multi-behavior map-elites},
  author={Anne, Timoth{\'e}e and Mouret, Jean-Baptiste},
  booktitle={Proceedings of the Companion Conference on Genetic and Evolutionary Computation},
  pages={111--114},
  year={2023}
}

@article{mouret2015illuminating,
  title={Illuminating search spaces by mapping elites},
  author={Mouret, Jean-Baptiste and Clune, Jeff},
  journal={arXiv preprint arXiv:1504.04909},
  year={2015}
}

@article{kumar2024automating,
  title={Automating the Search for Artificial Life with Foundation Models},
  author={Kumar, Akarsh and Lu, Chris and Kirsch, Louis and Tang, Yujin and Stanley, Kenneth O and Isola, Phillip and Ha, David},
  journal={arXiv preprint arXiv:2412.17799},
  year={2024}
}

@inproceedings{wang2020enhanced,
  title={Enhanced poet: Open-ended reinforcement learning through unbounded invention of learning challenges and their solutions},
  author={Wang, Rui and Lehman, Joel and Rawal, Aditya and Zhi, Jiale and Li, Yulun and Clune, Jeffrey and Stanley, Kenneth},
  booktitle={International conference on machine learning},
  pages={9940--9951},
  year={2020},
  organization={PMLR}
}

@article{kimura1979neutral,
  title={The neutral theory of molecular evolution},
  author={Kimura, Motoo},
  journal={Scientific American},
  volume={241},
  number={5},
  pages={98--129},
  year={1979},
  publisher={JSTOR}
}

@inproceedings{lehman2015enhancing,
  title={Enhancing divergent search through extinction events},
  author={Lehman, Joel and Miikkulainen, Risto},
  booktitle={Proceedings of the 2015 Annual Conference on Genetic and Evolutionary Computation},
  pages={951--958},
  year={2015}
}

@misc{jax2018github,
  author = {James Bradbury and Roy Frostig and Peter Hawkins and Matthew James Johnson and Chris Leary and Dougal Maclaurin and George Necula and Adam Paszke and Jake VanderPlas and Skye Wanderman-Milne and Qiao Zhang},
  title = {{JAX}: composable transformations of {P}ython+{N}um{P}y programs},
  version = {0.3.13},
  year = {2018},
}

@article{dawkins1979arms,
  title={Arms races between and within species},
  author={Dawkins, Richard and Krebs, John Richard},
  journal={Proceedings of the Royal Society of London. Series B. Biological Sciences},
  volume={205},
  number={1161},
  pages={489--511},
  year={1979},
  publisher={The Royal Society London}
}

@article{wan2024quality,
  title={Quality Diversity Imitation Learning},
  author={Wan, Zhenglin and Yu, Xingrui and Bossens, David Mark and Lyu, Yueming and Guo, Qing and Fan, Flint Xiaofeng and Tsang, Ivor},
  journal={arXiv preprint 2410.06151},
  year={2024}
}

@inproceedings{costa2020exploring,
  title={Exploring the evolution of gans through quality diversity},
  author={Costa, Victor and Lourenco, Nuno and Correia, Joao and Machado, Penousal},
  booktitle={Proceedings of the 2020 genetic and evolutionary computation conference},
  pages={297--305},
  year={2020}
}

@inproceedings{steckel2021illuminating,
  title={Illuminating the space of beatable lode runner levels produced by various generative adversarial networks},
  author={Steckel, Kirby and Schrum, Jacob},
  booktitle={Proceedings of the genetic and evolutionary computation conference companion},
  pages={111--112},
  year={2021}
}

@article{Samvelyan2024RainbowTOA,
  title={Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts},
  author={Samvelyan, Mikayel and Raparthy, S. and Lupu, Andrei and Hambro, Eric and Markosyan, Aram H. and Bhatt, Manish and Mao, Yuning and Jiang, Minqi and Parker-Holder, Jack and Foerster, Jakob and Rocktaschel, Tim and Raileanu, Roberta},
  journal={ArXiv},
  year={2024},
  volume={abs/2402.16822},
}

@inproceedings{ficici1998challenges,
  title={Challenges in coevolutionary learning: Arms-race dynamics, open-endedness, and mediocre stable states},
  author={Ficici, Sevan G and Pollack, Jordan B},
  booktitle={Proceedings of the sixth international conference on Artificial life},
  pages={238--247},
  year={1998},
  organization={MIT Press Cambridge, MA}
}

@inproceedings{wang2019poet,
  title={Poet: open-ended coevolution of environments and their optimized solutions},
  author={Wang, Rui and Lehman, Joel and Clune, Jeff and Stanley, Kenneth O},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference},
  pages={142--151},
  year={2019}
}

@inproceedings{baker2019emergent,
  title={Emergent tool use from multi-agent autocurricula},
  author={Baker, Bowen and Kanitscheider, Ingmar and Markov, Todor and Wu, Yi and Powell, Glenn and McGrew, Bob and Mordatch, Igor},
  booktitle={International conference on learning representations},
  year={2019}
}

@book{elo1978rating,
  author={Elo, Arpad E.},
  title={The Rating of Chessplayers, Past and Present},
  year={1978},
  publisher={Arco Publishing},
}

@inproceedings{dharna2024quality,
  title={Quality-Diversity Self-Play: Open-Ended Strategy Innovation via Foundation Models},
  author={Dharna, Aaron and Lu, Cong and Clune, Jeff},
  booktitle={NeurIPS 2024 Workshop on Open-World Agents},
  year={2024}
}

@inproceedings{brant2017minimal,
  title={Minimal criterion coevolution: a new approach to open-ended search},
  author={Brant, Jonathan C and Stanley, Kenneth O},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference},
  pages={67--74},
  year={2017}
}

@article{dolson2019modes,
  title={The MODES toolbox: Measurements of open-ended dynamics in evolving systems},
  author={Dolson, Emily L and Vostinar, Anya E and Wiser, Michael J and Ofria, Charles},
  journal={Artificial life},
  volume={25},
  number={1},
  pages={50--73},
  year={2019},
  publisher={MIT Press}
}

@inproceedings{soros2014identifying,
  title={Identifying necessary conditions for open-ended evolution through the artificial life world of chromaria},
  author={Soros, Lisa and Stanley, Kenneth},
  booktitle={Artificial Life Conference Proceedings},
  pages={793--800},
  year={2014},
}

@article{bedau2000open,
  title={Open problems in artificial life},
  author={Bedau, Mark A and McCaskill, John S and Packard, Norman H and Rasmussen, Steen and Adami, Chris and Green, David G and Ikegami, Takashi and Kaneko, Kunihiko and Ray, Thomas S},
  journal={Artificial life},
  volume={6},
  number={4},
  pages={363--376},
  year={2000},
}

@article{taylor2016open,
  title={Open-ended evolution: Perspectives from the OEE workshop in York},
  author={Taylor, Tim and Bedau, Mark and Channon, Alastair and Ackley, David and Banzhaf, Wolfgang and Beslon, Guillaume and Dolson, Emily and Froese, Tom and Hickinbotham, Simon and Ikegami, Takashi and others},
  journal={Artificial life},
  volume={22},
  number={3},
  pages={408--423},
  year={2016},
}

@article{packard2019overview,
  title={An overview of open-ended evolution: Editorial introduction to the open-ended evolution ii special issue},
  author={Packard, Norman and Bedau, Mark A and Channon, Alastair and Ikegami, Takashi and Rasmussen, Steen and Stanley, Kenneth O and Taylor, Tim},
  journal={Artificial life},
  volume={25},
  number={2},
  pages={93--103},
  year={2019},
}

@article{hintze2019open,
  title={Open-endedness for the sake of open-endedness},
  author={Hintze, Arend},
  journal={Artificial life},
  volume={25},
  number={2},
  pages={198--206},
  year={2019},
}

@article{stepney2021modelling,
  title={Modelling and measuring open-endedness},
  author={Stepney, Susan},
  journal={Artificial Life},
  volume={25},
  number={1},
  pages={9},
  year={2021}
}

@misc{dorin2024artificial,
  title={What Is Artificial Life Today, and Where Should It Go?},
  author={Dorin, Alan and Stepney, Susan},
  year={2024},
}

@article{witkowski2019make,
  title={How to make swarms open-ended? Evolving collective intelligence through a constricted exploration of adjacent possibles},
  author={Witkowski, Olaf and Ikegami, Takashi},
  journal={Artificial life},
  volume={25},
  number={2},
  pages={178--197},
  year={2019},
}

@article{harrington2019escalation,
  title={Escalation of memory length in finite populations},
  author={Harrington, Kyle and Pollack, Jordan},
  journal={Artificial life},
  volume={25},
  number={1},
  pages={22--32},
  year={2019},
}

@article{moran2019evolving,
  title={Evolving complexity in prediction games},
  author={Moran, Nick and Pollack, Jordan},
  journal={Artificial Life},
  volume={25},
  number={1},
  pages={74--91},
  year={2019},
}

@inproceedings{fontaine2019mapping,
  title={Mapping hearthstone deck spaces through map-elites with sliding boundaries},
  author={Fontaine, Matthew C and Lee, Scott and Soros, Lisa B and de Mesentier Silva, Fernando and Togelius, Julian and Hoover, Amy K},
  booktitle={Proceedings of The Genetic and Evolutionary Computation Conference},
  pages={161--169},
  year={2019}
}

@inproceedings{fontaine2020covariance,
  title={Covariance matrix adaptation for the rapid illumination of behavior space},
  author={Fontaine, Matthew C and Togelius, Julian and Nikolaidis, Stefanos and Hoover, Amy K},
  booktitle={Proceedings of the 2020 genetic and evolutionary computation conference},
  pages={94--102},
  year={2020}
}

@article{anne2025harnessing,
  title={Harnessing language for coordination: A framework and benchmark for llm-driven multi-agent control},
  author={Anne, Timothee and Syrkis, Noah and Elhosni, Meriem and Turati, Florian and Legendre, Franck and Jaquier, Alain and Risi, Sebastian},
  journal={IEEE Transactions on Games},
  year={2025},
}

@inproceedings{gavsperov2024finding,
  title={Finding Near-Optimal Portfolios with Quality-Diversity},
  author={Gasperov, Bruno and Durasevic, Marko and Jakobovic, Domagoj},
  booktitle={International Conference on the Applications of Evolutionary Computation},
  pages={3--18},
  year={2024},
}

@article{brevault2024bayesian,
  title={Bayesian Quality-Diversity approaches for constrained optimization problems with mixed continuous, discrete and categorical variables},
  author={Brevault, Loic and Balesdent, Mathieu},
  journal={Engineering Applications of Artificial Intelligence},
  volume={133},
  pages={108118},
  year={2024},
}

@inproceedings{mertan2023modular,
  title={Modular controllers facilitate the co-optimization of morphology and control in soft robots},
  author={Mertan, Alican and Cheney, Nick},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference},
  pages={174--183},
  year={2023}
}

@article{bhatia2021evolution,
  title={Evolution gym: A large-scale benchmark for evolving soft robots},
  author={Bhatia, Jagdeep and Jackson, Holly and Tian, Yunsheng and Xu, Jie and Matusik, Wojciech},
  journal={Advances in Neural Information Processing Systems},
  volume={34},
  pages={2201--2214},
  year={2021}
}

@inproceedings{kriegman2017minimal,
  title={A minimal developmental model can increase evolvability in soft robots},
  author={Kriegman, Sam and Cheney, Nick and Corucci, Francesco and Bongard, Josh C},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference},
  pages={131--138},
  year={2017}
}

@article{cheney2014unshackling,
  title={Unshackling evolution: evolving soft robots with multiple materials and a powerful generative encoding},
  author={Cheney, Nick and MacCurdy, Robert and Clune, Jeff and Lipson, Hod},
  journal={ACM SIGEVOlution},
  volume={7},
  number={1},
  pages={11--23},
  year={2014},
}

@article{sims1994evolving,
  title={Evolving 3D morphology and behavior by competition},
  author={Sims, Karl},
  journal={Artificial life},
  volume={1},
  number={4},
  pages={353--372},
  year={1994}
}

@inproceedings{bahlous2025dominated,
  title={Dominated Novelty Search: Rethinking Local Competition in Quality-Diversity},
  author={Bahlous-Boldi, Ryan and Faldor, Maxence and Grillotti, Luca and Janmohamed, Hannah and Coiffard, Lisa and Spector, Lee and Cully, Antoine},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference},
  pages={104--112},
  year={2025}
}

@article{cheney2018scalable,
  title={Scalable co-optimization of morphology and control in embodied machines},
  author={Cheney, Nick and Bongard, Josh and SunSpiral, Vytas and Lipson, Hod},
  journal={Journal of The Royal Society Interface},
  volume={15},
  number={143},
  pages={20170937},
  year={2018},
}

@book{langton1997artificial,
  title={Artificial life: An overview},
  author={Langton, Christopher G},
  year={1997},
  publisher={Mit press}
}

@misc{hearthbreaker,
  author={Daniel, Yule and others},
  title={Hearthbreaker: A Hearthstone Simulator},
  year={2014},
}

@inproceedings{santos2017monte,
  title={Monte carlo tree search experiments in hearthstone},
  author={Santos, Andre and Santos, Pedro A and Melo, Francisco S},
  booktitle={2017 IEEE conference on computational intelligence and games (CIG)},
  pages={272--279},
  year={2017},
}

@article{brooks1991intelligence,
  title={Intelligence without representation},
  author={Brooks, Rodney A},
  journal={Artificial intelligence},
  volume={47},
  number={1-3},
  pages={139--159},
  year={1991},
}

@book{pfeifer2006body,
  title={How the body shapes the way we think: a new view of intelligence},
  author={Pfeifer, Rolf and Bongard, Josh},
  year={2006},
  publisher={MIT press}
}

@article{anne2025adversarial,
  title={Generational Adversarial MAP-Elites for Multi-Agent Game Illumination},
  author={Anne, Timothee and Syrkis, Noah and Elhosni, Meriem and Turati, Florian and Legendre, Franck and Jaquier, Alain and Risi, Sebastian},
  journal={Accepted for presentation at ALIFE '25, Kyoto, Japan},
  year={2025}
}

@misc{hearthstone2014,
  title={Hearthstone: Heroes of Warcraft},
  author={{Blizzard Entertainment}},
  year={2014},
}

@misc{sabberStone,
  author={Milva and others},
  title={SabberStone},
  year={2016},
}

@inproceedings{chigot2022coevolution,
  title={Coevolution of neural networks for agents and environments},
  author={Chigot, Estelle and Wilson, Dennis G},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference Companion},
  pages={2306--2309},
  year={2022}
}

@inproceedings{faldoromni,
  title={OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code},
  author={Faldor, Maxence and Zhang, Jenny and Cully, Antoine and Clune, Jeff},
  booktitle={The Thirteenth International Conference on Learning Representations},
  year={2024}
}

@article{nadizar2025enhancing,
  title={Enhancing adaptability in embodied agents: A multi-quality-diversity approach},
  author={Nadizar, Giorgia and Medvet, Eric and Wilson, Dennis G},
  journal={IEEE Transactions on Evolutionary Computation},
  year={2025},
}

@book{elo1978rating,
  address = {New York},
  author = {Elo, Arpad E.},
  isbn = {0668047216 9780668047210},
  keywords = {cati},
  publisher = {Arco Pub.},
  refid = {4504131},
  title = {The Rating of Chessplayers, Past and Present},
  year = 1978
}

@book{osborne2004introduction,
  title={An introduction to game theory},
  author={Osborne, Martin J and others},
  volume={3},
  number={3},
  year={2004},
  publisher={Springer}
}

@inproceedings{anne2025generational,
  title={Generational Adversarial MAP-Elites for Multi-Agent Game Illumination},
  author={Anne, Timoth{\'e}e and Syrkis, Noah and Elhosni, Meriem and Turati, Florian and Legendre, Franck and Jaquier, Alain and Risi, Sebastian},
  booktitle={Artificial Life Conference Proceedings 37},
  volume={2025},
  number={1},
  pages={31},
  year={2025},
  organization={MIT Press One Rogers Street, Cambridge, MA 02142-1209, USA journals-info~…}
}

@inproceedings{anne2023multi,
  title={Multi-task multi-behavior map-elites},
  author={Anne, Timoth{\'e}e and Mouret, Jean-Baptiste},
  booktitle={Proceedings of the companion conference on genetic and evolutionary computation},
  pages={111--114},
  year={2023}
}



@article{deb2013evolutionary,
  title={An evolutionary many-objective optimization algorithm using reference-point-based nondominated sorting approach, part I: solving problems with box constraints},
  author={Deb, Kalyanmoy and Jain, Himanshu},
  journal={IEEE transactions on evolutionary computation},
  volume={18},
  number={4},
  pages={577--601},
  year={2013},
  publisher={IEEE}
}


@inproceedings{radford2021learning,
  title={Learning transferable visual models from natural language supervision},
  author={Radford, Alec and Kim, Jong Wook and Hallacy, Chris and Ramesh, Aditya and Goh, Gabriel and Agarwal, Sandhini and Sastry, Girish and Askell, Amanda and Mishkin, Pamela and Clark, Jack and others},
  booktitle={International conference on machine learning},
  pages={8748--8763},
  year={2021},
  organization={PmLR}
}


@misc{jax2018github,
  author = {James Bradbury and Roy Frostig and Peter Hawkins and Matthew James Johnson and Chris Leary and Dougal Maclaurin and George Necula and Adam Paszke and Jake Vander{P}las and Skye Wanderman-{M}ilne and Qiao Zhang},
  title = {{JAX}: composable transformations of {P}ython+{N}um{P}y programs},
  version = {0.3.13},
  year = {2018},
}

@book{isaacs1999differential,
  title={Differential games: a mathematical theory with applications to warfare and pursuit, control and optimization},
  author={Isaacs, Rufus},
  year={1999},
  publisher={Courier Corporation}
}

@article{dawkins1979arms,
  title={Arms races between and within species},
  author={Dawkins, Richard and Krebs, John Richard},
  journal={Proceedings of the Royal Society of London. Series B. Biological Sciences},
  volume={205},
  number={1161},
  pages={489--511},
  year={1979},
  publisher={The Royal Society London}
}

@inproceedings{ficici1998challenges,
  title={Challenges in coevolutionary learning: Arms-race dynamics, open-endedness, and mediocre stable states},
  author={Ficici, Sevan G and Pollack, Jordan B},
  booktitle={Proceedings of the sixth international conference on Artificial life},
  pages={238--247},
  year={1998},
  organization={MIT Press Cambridge, MA}
}

@inproceedings{wang2019poet,
  title={Poet: open-ended coevolution of environments and their optimized solutions},
  author={Wang, Rui and Lehman, Joel and Clune, Jeff and Stanley, Kenneth O},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference},
  pages={142--151},
  year={2019}
}

@inproceedings{wang2020enhanced,
  title={Enhanced poet: Open-ended reinforcement learning through unbounded invention of learning challenges and their solutions},
  author={Wang, Rui and Lehman, Joel and Rawal, Aditya and Zhi, Jiale and Li, Yulun and Clune, Jeffrey and Stanley, Kenneth},
  booktitle={International conference on machine learning},
  pages={9940--9951},
  year={2020},
  organization={PMLR}
}

@article{vinyals2019grandmaster,
  title={Grandmaster level in StarCraft II using multi-agent reinforcement learning},
  author={Vinyals, Oriol and Babuschkin, Igor and Czarnecki, Wojciech M and Mathieu, Micha{\"e}l and Dudzik, Andrew and Chung, Junyoung and Choi, David H and Powell, Richard and Ewalds, Timo and Georgiev, Petko and others},
  journal={nature},
  volume={575},
  number={7782},
  pages={350--354},
  year={2019},
  publisher={Nature Publishing Group}
}

@inproceedings{baker2019emergent,
  title={Emergent tool use from multi-agent autocurricula},
  author={Baker, Bowen and Kanitscheider, Ingmar and Markov, Todor and Wu, Yi and Powell, Glenn and McGrew, Bob and Mordatch, Igor},
  booktitle={International conference on learning representations},
  year={2019}
}

@inproceedings{lehman2011evolving,
  title={Evolving a diversity of virtual creatures through novelty search and local competition},
  author={Lehman, Joel and Stanley, Kenneth O},
  booktitle={Proceedings of the 13th annual conference on Genetic and evolutionary computation},
  pages={211--218},
  year={2011}
}


@article{mouret2015illuminating,
  title={Illuminating search spaces by mapping elites},
  author={Mouret, Jean-Baptiste and Clune, Jeff},
  journal={arXiv preprint arXiv:1504.04909},
  year={2015}
}

@inproceedings{mouret2020quality,
  title={Quality diversity for multi-task optimization},
  author={Mouret, Jean-Baptiste and Maguire, Glenn},
  booktitle={Proceedings of the 2020 Genetic and Evolutionary Computation Conference},
  pages={121--129},
  year={2020}
}

@inproceedings{fontaine2019mapping,
  title={Mapping hearthstone deck spaces through map-elites with sliding boundaries},
  author={Fontaine, Matthew C and Lee, Scott and Soros, Lisa B and de Mesentier Silva, Fernando and Togelius, Julian and Hoover, Amy K},
  booktitle={Proceedings of The Genetic and Evolutionary Computation Conference},
  pages={161--169},
  year={2019}
}


@misc{hearthstone2014,
  title        = {Hearthstone: Heroes of Warcraft},
  author       = {{Blizzard Entertainment}},
  year         = {2014},
  publisher    = {{Blizzard Entertainment}},
  note         = {Digital collectible card game},
  url          = {https://playhearthstone.com/},
}

@inproceedings{fontaine2020covariance,
  title={Covariance matrix adaptation for the rapid illumination of behavior space},
  author={Fontaine, Matthew C and Togelius, Julian and Nikolaidis, Stefanos and Hoover, Amy K},
  booktitle={Proceedings of the 2020 genetic and evolutionary computation conference},
  pages={94--102},
  year={2020}
}

@inproceedings{steckel2021illuminating,
  title={Illuminating the space of beatable lode runner levels produced by various generative adversarial networks},
  author={Steckel, Kirby and Schrum, Jacob},
  booktitle={Proceedings of the genetic and evolutionary computation conference companion},
  pages={111--112},
  year={2021}
}

@article{Samvelyan2024RainbowTOA,
  title={Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts},
  author={Mikayel Samvelyan and S. Raparthy and Andrei Lupu and Eric Hambro and Aram H. Markosyan and Manish Bhatt and Yuning Mao and Minqi Jiang and Jack Parker-Holder and Jakob Foerster and Tim Rocktaschel and Roberta Raileanu},
  journal={ArXiv},
  year={2024},
  volume={abs/2402.16822},
  url={https://api.semanticscholar.org/CorpusId:268031888}
}

@article{wan2024quality,
  title={Quality Diversity Imitation Learning},
  author={Wan, Zhenglin and Yu, Xingrui and Bossens, David Mark and Lyu, Yueming and Guo, Qing and Fan, Flint Xiaofeng and Tsang, Ivor},
  journal={arXiv preprint arXiv:2410.06151},
  year={2024}
}

@article{samvelyan2024multi,
  title={Multi-agent diagnostics for robustness via illuminated diversity},
  author={Samvelyan, Mikayel and Paglieri, Davide and Jiang, Minqi and Parker-Holder, Jack and Rockt{\"a}schel, Tim},
  journal={arXiv preprint arXiv:2401.13460},
  year={2024}
}


@inproceedings{costa2020exploring,
  title={Exploring the evolution of gans through quality diversity},
  author={Costa, Victor and Lourenco, Nuno and Correia, Joao and Machado, Penousal},
  booktitle={Proceedings of the 2020 genetic and evolutionary computation conference},
  pages={297--305},
  year={2020}
}

@inproceedings{dharna2024quality,
  title={Quality-Diversity Self-Play: Open-Ended Strategy Innovation via Foundation Models},
  author={Dharna, Aaron and Lu, Cong and Clune, Jeff},
  booktitle={NeurIPS 2024 Workshop on Open-World Agents},
  year={2024}
}

@article{kumar2024automating,
  title={Automating the Search for Artificial Life with Foundation Models},
  author={Kumar, Akarsh and Lu, Chris and Kirsch, Louis and Tang, Yujin and Stanley, Kenneth O and Isola, Phillip and Ha, David},
  journal={arXiv preprint arXiv:2412.17799},
  year={2024}
}

@inproceedings{chigot2022coevolution,
  title={Coevolution of neural networks for agents and environments},
  author={Chigot, Estelle and Wilson, Dennis G},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference Companion},
  pages={2306--2309},
  year={2022}
}

@inproceedings{faldoromni,
  title={OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code},
  author={Faldor, Maxence and Zhang, Jenny and Cully, Antoine and Clune, Jeff},
  booktitle={The Thirteenth International Conference on Learning Representations},
  year={2024}
}

@article{nadizar2025enhancing,
  title={Enhancing adaptability in embodied agents: A multi-quality-diversity approach},
  author={Nadizar, Giorgia and Medvet, Eric and Wilson, Dennis G},
  journal={IEEE Transactions on Evolutionary Computation},
  year={2025},
  publisher={IEEE}
}

@article{kumar2026digital,
  title={Digital Red Queen: Adversarial Program Evolution in Core War with LLMs},
  author={Kumar, Akarsh and Bahlous-Boldi, Ryan and Sharma, Prafull and Isola, Phillip and Risi, Sebastian and Tang, Yujin and Ha, David},
  journal={arXiv preprint arXiv:2601.03335},
  year={2026}
}

@article{zhang2024survey,
  title={A survey on self-play methods in reinforcement learning},
  author={Zhang, Ruize and Xu, Zelai and Ma, Chengdong and Yu, Chao and Tu, Wei-Wei and Tang, Wenhao and Huang, Shiyu and Ye, Deheng and Ding, Wenbo and Yang, Yaodong and others},
  journal={arXiv preprint arXiv:2408.01072},
  year={2024}
}

@article{dang2025rainbowplus,
  title={RainbowPlus: Enhancing Adversarial Prompt Generation via Evolutionary Quality-Diversity Search},
  author={Dang, Quy-Anh and Ngo, Chris and Hy, Truong-Son},
  journal={arXiv preprint arXiv:2504.15047},
  year={2025}
}

@article{wang2025quality,
  title={Quality-Diversity Red-Teaming: Automated Generation of High-Quality and Diverse Attackers for Large Language Models},
  author={Wang, Ren-Jian and Xue, Ke and Qin, Zeyu and Li, Ziniu and Tang, Sheng and Li, Hao-Tian and Liu, Shengcai and Qian, Chao},
  journal={arXiv preprint arXiv:2506.07121},
  year={2025}
}

@inproceedings{nguyen2025diversifying,
  title={Diversifying Adversarial Attacks on Text-to-image Generation},
  author={Nguyen, Thai Huy and Luong, Ngoc Hoang},
  booktitle={Proceedings of the Genetic and Evolutionary Computation Conference Companion},
  pages={315--318},
  year={2025}
}

@article{pugh2016quality,
  title={Quality diversity: A new frontier for evolutionary computation},
  author={Pugh, Justin K and Soros, Lisa B and Stanley, Kenneth O},
  journal={Frontiers in Robotics and AI},
  volume={3},
  pages={40},
  year={2016},
  publisher={Frontiers Media SA}
}

@article{zhao2023survey,
  title={A survey of large language models},
  author={Zhao, Wayne Xin and Zhou, Kun and Li, Junyi and Tang, Tianyi and Wang, Xiaolei and Hou, Yupeng and Min, Yingqian and Zhang, Beichen and Zhang, Junjie and Dong, Zican and others},
  journal={arXiv preprint arXiv:2303.18223},
  volume={1},
  number={2},
  year={2023}
}

@article{silver2017mastering,
  title={Mastering the game of go without human knowledge},
  author={Silver, David and Schrittwieser, Julian and Simonyan, Karen and Antonoglou, Ioannis and Huang, Aja and Guez, Arthur and Hubert, Thomas and Baker, Lucas and Lai, Matthew and Bolton, Adrian and others},
  journal={nature},
  volume={550},
  number={7676},
  pages={354--359},
  year={2017},
  publisher={Nature Publishing Group UK London}
}

@article{berner2019dota,
  title={Dota 2 with large scale deep reinforcement learning},
  author={Berner, Christopher and Brockman, Greg and Chan, Brooke and Cheung, Vicki and Debiak, Przemyslaw and Dennison, Christy and Farhi, David and Fischer, Quirin and Hashme, Shariq and Hesse, Chris and others},
  journal={arXiv preprint arXiv:1912.06680},
  year={2019}
}

@article{bedau2000open,
  title={Open problems in artificial life},
  author={Bedau, Mark A and McCaskill, John S and Packard, Norman H and Rasmussen, Steen and Adami, Chris and Green, David G and Ikegami, Takashi and Kaneko, Kunihiko and Ray, Thomas S},
  journal={Artificial life},
  volume={6},
  number={4},
  pages={363--376},
  year={2000},
  publisher={MIT Press}
}

@misc{dorin2024artificial,
  title={What Is Artificial Life Today, and Where Should It Go?},
  author={Dorin, Alan and Stepney, Susan},
  journal={Artificial Life},
  volume={30},
  number={1},
  pages={1--15},
  year={2024},
  publisher={MIT Press One Broadway, 12th Floor, Cambridge, Massachusetts 02142, USA~…}
}

@article{moran2019evolving,
  title={Evolving complexity in prediction games},
  author={Moran, Nick and Pollack, Jordan},
  journal={Artificial Life},
  volume={25},
  number={1},
  pages={74--91},
  year={2019},
  publisher={MIT Press One Rogers Street, Cambridge, MA 02142-1209, USA journals-info~…}
}

@article{harrington2019escalation,
  title={Escalation of memory length in finite populations},
  author={Harrington, Kyle and Pollack, Jordan},
  journal={Artificial life},
  volume={25},
  number={1},
  pages={22--32},
  year={2019},
  publisher={MIT Press}
}

@article{cully2015robots,
  title={Robots that can adapt like animals},
  author={Cully, Antoine and Clune, Jeff and Tarapore, Danesh and Mouret, Jean-Baptiste},
  journal={Nature},
  volume={521},
  number={7553},
  pages={503--507},
  year={2015},
  publisher={Nature Publishing Group UK London}
}

@article{jiang2022artificial,
  title={An artificial intelligence enabled chemical synthesis robot for exploration and optimization of nanomaterials},
  author={Jiang, Yibin and Salley, Daniel and Sharma, Abhishek and Keenan, Graham and Mullin, Margaret and Cronin, Leroy},
  journal={Science advances},
  volume={8},
  number={40},
  pages={eabo2626},
  year={2022},
  publisher={American Association for the Advancement of Science}
}

@inproceedings{gravina2019procedural,
  title={Procedural content generation through quality diversity},
  author={Gravina, Daniele and Khalifa, Ahmed and Liapis, Antonios and Togelius, Julian and Yannakakis, Georgios N},
  booktitle={2019 IEEE Conference on Games (CoG)},
  pages={1--8},
  year={2019},
  organization={IEEE}
}

@article{brevault2024bayesian,
  title={Bayesian Quality-Diversity approaches for constrained optimization problems with mixed continuous, discrete and categorical variables},
  author={Brevault, Loic and Balesdent, Mathieu},
  journal={Engineering Applications of Artificial Intelligence},
  volume={133},
  pages={108118},
  year={2024},
  publisher={Elsevier}
}

@article{ganguli2022red,
  title={Red teaming language models to reduce harms: Methods, scaling behaviors, and lessons learned},
  author={Ganguli, Deep and Lovitt, Liane and Kernion, Jackson and Askell, Amanda and Bai, Yuntao and Kadavath, Saurav and Mann, Ben and Perez, Ethan and Schiefer, Nicholas and Ndousse, Kamal and others},
  journal={arXiv preprint arXiv:2209.07858},
  year={2022}
}

@book{elo1978rating,
  address = {New York},
  author = {Elo, Arpad E.},
  isbn = {0668047216 9780668047210},
  keywords = {cati},
  publisher = {Arco Pub.},
  refid = {4504131},
  title = {The Rating of Chessplayers, Past and Present},
  year = 1978
}

@book{osborne2004introduction,
  title={An introduction to game theory},
  author={Osborne, Martin J and others},
  volume={3},
  number={3},
  year={2004},
  publisher={Springer}
}

"""

import re

def clean_latex(s):
    """Remove common LaTeX commands and braces."""
    # Remove {\"x} style accents -> just x
    s = re.sub(r'\{\\["\'^`~=.]\s*(\w)\}', r'\1', s)
    s = re.sub(r'\\["\'^`~=.](\w)', r'\1', s)
    # Remove \'{x} etc.
    s = re.sub(r"\\'\{(\w+)\}", r'\1', s)
    s = re.sub(r'\{\\\'(\w+)\}', r'\1', s)
    # Handle {{Blizzard Entertainment}} -> Blizzard Entertainment
    s = re.sub(r'\{\{(.+?)\}\}', r'\1', s)
    # Remove remaining braces
    s = s.replace('{', '').replace('}', '')
    # Collapse whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_authors(raw):
    """Parse BibTeX author string into a list of 'First Last' strings."""
    raw = clean_latex(raw)
    parts = re.split(r'\s+and\s+', raw, flags=re.IGNORECASE)
    authors = []
    for p in parts:
        p = p.strip()
        if p.lower() == 'others':
            authors.append('et al.')
            continue
        if ',' in p:
            last, first = p.split(',', 1)
            authors.append(f"{first.strip()} {last.strip()}")
        else:
            authors.append(p)
    return authors

def format_authors(authors):
    """Format author list as 'F. Last, F. Last, and F. Last'."""
    def abbrev(name):
        if name == 'et al.':
            return 'et al.'
        tokens = name.split()
        if not tokens:
            return name
        last = tokens[-1]
        initials = ' '.join(t[0] + '.' for t in tokens[:-1] if t)
        return f"{initials} {last}".strip()

    abbreviated = [abbrev(a) for a in authors]
    if len(abbreviated) == 1:
        return abbreviated[0]
    elif len(abbreviated) == 2:
        return f"{abbreviated[0]} and {abbreviated[1]}"
    else:
        return ', '.join(abbreviated[:-1]) + ', and ' + abbreviated[-1]

def get_field(entry_body, field):
    """Extract a field value from the entry body."""
    pattern = rf'^\s*{field}\s*=\s*[{{"](.+?)[}}"]\s*[,}}]?$'
    m = re.search(pattern, entry_body, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if m:
        val = m.group(1).strip()
        # handle multiline
        val = re.sub(r'\s+', ' ', val)
        return val
    return ''

def format_pages(pages):
    pages = pages.replace('--', '–')
    return pages

def format_entry(label, etype, body):
    title = clean_latex(get_field(body, 'title'))
    raw_authors = get_field(body, 'author')
    year = get_field(body, 'year')
    authors_list = parse_authors(raw_authors) if raw_authors else []
    authors_str = format_authors(authors_list)

    etype = etype.lower()

    if etype in ('article',):
        journal = clean_latex(get_field(body, 'journal'))
        volume = get_field(body, 'volume')
        number = get_field(body, 'number')
        pages = format_pages(get_field(body, 'pages'))
        parts = [f'{authors_str}, {title},', journal + ',']
        if volume:
            vol_str = f'vol. {volume}'
            if number:
                vol_str += f', no. {number}'
            parts.append(vol_str + ',')
        if pages:
            parts.append(f'pp. {pages},')
        parts.append(f'{year}.')
        ref = ' '.join(parts)

    elif etype in ('inproceedings', 'conference'):
        booktitle = clean_latex(get_field(body, 'booktitle'))
        pages = format_pages(get_field(body, 'pages'))
        parts = [f'{authors_str}, {title},', f'in {booktitle},']
        if pages:
            parts.append(f'pp. {pages},')
        parts.append(f'{year}.')
        ref = ' '.join(parts)

    elif etype == 'book':
        publisher = clean_latex(get_field(body, 'publisher'))
        parts = [f'{authors_str}, {title}.', publisher + ',', f'{year}.']
        ref = ' '.join(parts)

    elif etype == 'misc':
        title_f = clean_latex(get_field(body, 'title'))
        howpub = clean_latex(get_field(body, 'howpublished'))
        url = clean_latex(get_field(body, 'url'))
        parts = [f'{authors_str}, {title_f},']
        if howpub:
            parts.append(howpub + ',')
        elif url:
            parts.append(url + ',')
        parts.append(f'{year}.')
        ref = ' '.join(parts)

    else:
        # fallback
        ref = f'{authors_str}, {title}, {year}.'

    return f'{label}: "{ref}"'


def parse_bib(bib_text):
    results = []
    pattern = re.compile(
        r'@(\w+)\s*\{\s*([^,\s]+)\s*,(.+?)\n\}',
        re.DOTALL
    )
    labels = set()
    for m in pattern.finditer(bib_text):
        etype, label, body = m.group(1), m.group(2), m.group(3)
        if label not in labels:
            labels.add(label)
            results.append(format_entry(label, etype, body))
    return results


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            bib_text = f.read()
    else:
        bib_text = BIB

    entries = parse_bib(bib_text)
    for e in entries:
        print(e)