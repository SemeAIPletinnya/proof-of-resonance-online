import numpy as np

class MultimodalResonance:
    def __init__(self, alpha=0.1, steps=150):
        self.alpha = alpha
        self.steps = steps

    def resonate(self, img_vec, txt_vec):
        img = img_vec.copy()
        txt = txt_vec.copy()
        history = []

        for _ in range(self.steps):
            delta = (img - txt)
            img -= self.alpha * delta
            txt += self.alpha * delta
            history.append(np.linalg.norm(img - txt))

        return img, txt, history
