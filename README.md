# Life on Mars?
## [NIPS Workshop on Machine Learning for Creativity and Design](https://nips.cc/Conferences/2018/Schedule?showEvent=10924)
This work is a submission to the [NIPS Workshop on Machine Learning for Creativity and Design](https://nips.cc/Conferences/2018/Schedule?showEvent=10924).

## Team

| ![Stephen Solis][StephenSolis-photo]  | ![Albert Jimenez][AlbertJimenez-photo]  |  ![Adria Romero][AdriaRomero-photo] | ![Mohamed Akrout][MohamedAkrout-photo] | ![Anirudh Challa][AnirudhChalla-photo] |
|:-:|:-:|:-:|:-:|:-:|
| [Stephen Solis][StephenSolis-web]  | [Albert Jimenez][AlbertJimenez-web] | [Adria Romero][AdriaRomero-web] | [Mohamed Akrout][MohamedAkrout-web] |  [Anirudh Challa][AnirudhChalla-web] | 

[StephenSolis-photo]: https://user-images.githubusercontent.com/12190870/47591238-dc2cf880-d93c-11e8-9885-dcced755bcf8.png
[AlbertJimenez-photo]: https://user-images.githubusercontent.com/5657335/47261794-9e941f80-d4a5-11e8-8850-7add90e97944.png
[AdriaRomero-photo]: https://user-images.githubusercontent.com/5657335/47261792-9a680200-d4a5-11e8-9982-df7f8069dc31.png
[MohamedAkrout-photo]: https://user-images.githubusercontent.com/5657335/47261796-a18f1000-d4a5-11e8-9924-3b2008fa604c.png
[AnirudhChalla-photo]: https://user-images.githubusercontent.com/5657335/47261797-a358d380-d4a5-11e8-9d7c-ff95d3f371bb.png


[StephenSolis-web]: https://stephensol.is/
[AlbertJimenez-web]: https://jsalbert.github.io/
[AdriaRomero-web]: http://adriaromero.net/
[MohamedAkrout-web]: https://www.linkedin.com/in/mohamed-akrout/
[AnirudhChalla-web]: https://www.linkedin.com/in/anirudhchalla2907/

## Abstract
Is there life on Mars? David Bowie was not the only human to have ever wondered about the existence of life on the red planet. Regardless of whether it’s possible or not, how might we imagine human civilization on Mars? 

This project attempts to present an artistic representation of Mars after undergoing terraforming by humans. As a result of this planetary engineering technique, Mars’s surface would adopt a more habitable appearance, similar to that of the Earth. As an atmosphere is built and temperatures rise, the water cycle begins to take form. Clouds develop, mountains become covered in snow, rivers start flowing down to the green covered fields, and the rocky Martian deserts are replaced by trees and forests.

The recreation of that process was performed using an approach based on image to image translation trained on a dataset based on images of Earth and Mars (fiction and NASA).

## Technical description
There has been a lot of work in image (synthetic) generation using Artificial Intelligence in the last couple of years, but this work is distinguished from the rest since its novelty in the application of these state-of-the-art technologies to satellite and planet images. These methods are popularly known as [Neural Style Transfer](https://arxiv.org/abs/1508.06576), where the model is exposed to two domains: (1) the *content domain*, and (2) the *style reference domain*. After a training process, the model has learned the main features from the two domains, and it can act as a "styler" such that we present an input image, it transforms it to look like the content image (in this case Earth images), but “painted” in the appearance of the style reference domain.

## Results

| Original  | Styled |
| ------------- | ------------- |
| ![](https://raw.githubusercontent.com/stephensolis/life-on-mars/master/docs/assets/img/1_orig.jpg)  | ![](https://raw.githubusercontent.com/stephensolis/life-on-mars/master/docs/assets/img/1_select.jpg) |
| ![](https://raw.githubusercontent.com/stephensolis/life-on-mars/master/docs/assets/img/2_orig.jpg)  | ![](https://raw.githubusercontent.com/stephensolis/life-on-mars/master/docs/assets/img/2_select.jpg) |
| ![](https://raw.githubusercontent.com/stephensolis/life-on-mars/master/docs/assets/img/3_orig.jpg)  | ![](https://raw.githubusercontent.com/stephensolis/life-on-mars/master/docs/assets/img/3_select.jpg) |
| ![](https://raw.githubusercontent.com/stephensolis/life-on-mars/master/docs/assets/img/4_orig.jpg)  | ![](https://raw.githubusercontent.com/stephensolis/life-on-mars/master/docs/assets/img/4_select.jpg) |
