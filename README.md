# [Fairness Evaluation in Deepfake Detection Models using Metamorphic Testing](https://dl.acm.org/doi/abs/10.1145/3524846.3527337)
In this work, We have chosen [MesoInception-4](https://github.com/DariusAf/MesoNet), a state-of-the-art deepfake detection model, as the target model and makeup as the anomalies. Makeups are applied through utilizing the Dlib library to obtain the 68 facial landmarks prior to filling in the RGB values. Metamorphic relations are derived based on the notion that realistic perturbations of the input images, such as makeup, involving eyeliners, eyeshadows, blushes, and lipsticks (which are common cosmetic appearance) applied to male and female images, should not alter the output of the model by a huge margin. Furthermore, we narrow down the scope to focus on revealing potential gender biases in DL and AI systems. Specifically, we are interested to examine whether MesoInception-4 model produces unfair decisions, which should be considered as a consequence of robustness issues. The findings from our work have the potential to pave the way for new research directions in the quality assurance and fairness in DL and AI systems.

We transform the source test case obtianed from [Faceforensics](https://github.com/ondyari/FaceForensics) to construct the corresponding follow-up test cases, and propose the following metamorphic relations:
![Screenshot 2024-07-24 at 21 16 09](https://github.com/user-attachments/assets/34a47524-5e94-426e-a4e9-2b78213acffe)

Here are samples of makeup images in different test cases with contrast to the original image:
![Screenshot 2024-07-24 at 21 09 40](https://github.com/user-attachments/assets/c4ffb786-d391-4faf-a800-592a7b38e963)

## License
The code is released under the MIT license.
