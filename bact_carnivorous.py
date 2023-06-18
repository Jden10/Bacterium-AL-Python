import pygame as pg
from options import *
import random
import AI as ai


# ��������� ������ �� ���������� ��������
def get_r_obj(data, obj):
    dist = {}
    if len(data) != 0:
        for i in data:
            if i != obj:
                r = ((obj.rect.centerx - i.rect.centerx) ** 2 + (obj.rect.centery - i.rect.centery) ** 2) ** 0.5
                if r <= obj.visibil:
                    dist.setdefault(r, i)
        dist = dict(sorted(dist.items()))
    out_dist = [[i.rect.centerx - obj.rect.centerx, i.rect.centery - obj.rect.centery] for i in
                   dist.values()]  # �������������� ��� ������ � ���������
    return out_dist


class Bact(pg.sprite.Sprite):
    def __init__(self, x, y, weight):
        pg.sprite.Sprite.__init__(self)

        # ��������� ��������
        self.orig_image = pg.Surface((cell_bact, cell_bact))
        self.orig_image.fill('purple')
        pg.draw.circle(self.orig_image, color_bact_omn, (cell_bact // 2, cell_bact // 2), cell_bact // 2)  # ���� ��������
        pg.draw.circle(self.orig_image, 'white', (cell_bact // 10 * 3, cell_bact // 2), cell_bact // 6)  # ����� ������
        pg.draw.circle(self.orig_image, 'white', (cell_bact // 10 * 7, cell_bact // 2), cell_bact // 6)  # ������ ������
        pg.draw.circle(self.orig_image, 'black', (cell_bact // 10 * 3, cell_bact // 2), cell_bact // 15)  # ����� ������
        pg.draw.circle(self.orig_image, 'black', (cell_bact // 10 * 7, cell_bact // 2),
                       cell_bact // 15)  # ������ ������
        self.orig_image.set_colorkey('purple')
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=(x, y))

        # ��������� ��������
        self.radius = cell_bact // 2
        self.visibil = self.radius * 40
        self.energy = life_bacts
        self.coin = 0
        self.weight = weight
        self.old_x = 0
        self.old_y = 0
        self.timer = 0
        self.absorb = 0
        self.counter = 1
        self.vecx = 0
        self.vecy = 0


    def update(self, bacts_herb, bacts_omn, foods):
        # ������ ������������� �� ���������� ���������� (����������:��������)
        r_bact_herb = get_r_obj(bacts_herb, self)
        r_bact_omn = get_r_obj(bacts_omn, self)
        # ������ ������������� �� ���������� ���������� (����������:���)
        r_food = get_r_obj(foods, self)
        # �������� � ���������, ��������� ������� ��������
        center_ai = ai.get_output(ai.get_input(r_food, r_bact_herb, r_bact_omn), self.weight)

        # �������� ��������
        self.rect.centerx += center_ai[0][0]
        self.rect.centery += center_ai[0][1]

        # COIN �������� �� �������� ��������
        if self.rect.centerx == self.old_x and self.rect.centery == self.old_y:
            self.coin -= 5
        else:
            self.coin -= 1

        # COIN �������� ������ �� ������� ������
        if self.rect.centerx > width or self.rect.centerx < 0 or self.rect.centery > height or self.rect.centery < 0:
            self.coin -= 50
            self.energy = 0

        # COIN �������� ������������ � ����
        hits_food = pg.sprite.spritecollide(self, foods, True, pg.sprite.collide_circle)
        if hits_food:
            self.absorb += 1
            self.energy += life_bacts * 0.3
            self.coin += 20

        # COIN �������� ������������ � �����������
        hits_bact_h = pg.sprite.spritecollide(self, bacts_herb, True, pg.sprite.collide_circle)
        if hits_bact_h:
            self.absorb += 2
            self.energy += life_bacts * 0.4
            self.coin += 45

        # �������� ����������� �������
        if self.energy >= life_bacts:
            self.energy = life_bacts

        # ������ ��������� ����������
        self.vecx = self.rect.centerx + (self.old_x - self.rect.centerx) * self.radius
        self.vecy = self.rect.centery + (self.old_y - self.rect.centery) * self.radius
        self.old_x = self.rect.centerx
        self.old_y = self.rect.centery
        self.timer += 1 / FPS

        # �������� ������� � �������
        if self.timer >= self.counter:
            self.energy -= life_bacts * 0.35
            self.counter += 1


        # ������������ ��������
        bact_collide = pg.sprite.Group(i for i in bacts_omn)
        if self in bact_collide:
             bact_collide.remove(self)
        hits_bact = pg.sprite.spritecollide(self, bact_collide, False, pg.sprite.collide_circle)
        if hits_bact:
            for i in hits_bact:
                vec_colisx = (self.rect.centerx - i.rect.centerx)/2
                vec_colisy = (self.rect.centery - i.rect.centery)/2
                self.rect.centerx += vec_colisx
                self.rect.centery += vec_colisy


    # ������ ��������
    def death(self):
        if self.energy <= 0:
            self.kill()
            return [self.coin , [self.timer, self.weight]]

    # ����������� ��������
    def seed(self):
        if self.energy >= life_bacts // 1.5 and self.absorb >= 5:
            self.energy /= 1.5
            self.absorb = 0
            return [Bact(self.vecx, self.vecy, ai.change_best_weight(self.weight))]






# �������� �������� � ���������� �����
def create_bact(weight, qua):
    ret = []
    for _ in range(qua):
        x_rand = random.randint(0 + cell_bact, width - cell_bact)
        y_rand = random.randint(0 + cell_bact, height - cell_bact)
        ret.append(Bact(x_rand, y_rand, weight))
    return ret


# �������� ������ ���������
def create_gen_bact(qua, coin_bact, way):
    ret = []
    coin_bact = dict(sorted(coin_bact.items(), reverse=True))
    weight = [i[1] for i in coin_bact.values()]
    if way == 1:
        # �����e �� ��������� ��� �������
        while len(weight) <= round(qua * 0.4):
            weight.append(weight[len(weight) - 1])
        for i in range(round(qua * 0.4)):
            x_rand = random.randint(0 + cell_bact, width - cell_bact)
            y_rand = random.randint(0 + cell_bact, height - cell_bact)
            ret.append(Bact(x_rand, y_rand, weight[i]))
        # ������������ ���� ������
        x_rand = random.randint(0 + cell_bact, width - cell_bact)
        y_rand = random.randint(0 + cell_bact, height - cell_bact)
        ret.append(Bact(x_rand, y_rand, ai.change_best_weight(ai.mutation_two(weight[0], weight[1]))))
        # n �������������� �� 4 ��������� ������
        for i in range(round(qua * 0.3)):
            x_rand = random.randint(0 + cell_bact, width - cell_bact)
            y_rand = random.randint(0 + cell_bact, height - cell_bact)
            f1 = random.randint(0, round(len(weight) * 0.4))
            f2 = random.randint(0, round(len(weight) * 0.4))
            while f1 == f2:
                f2 = random.randint(0, round(len(weight) * 0.4))
            ret.append(Bact(x_rand, y_rand, ai.change_best_weight(ai.mutation_two(weight[f1], weight[f2]))))

        for i in range(round(qua * 0.2)):
            x_rand = random.randint(0 + cell_bact, width - cell_bact)
            y_rand = random.randint(0 + cell_bact, height - cell_bact)
            ret.append(Bact(x_rand, y_rand, ai.change_best_weight(weight[i])))
        return ret
    if way == 2:
        for _ in range(qua):
            x_rand = random.randint(0 + cell_bact, width - cell_bact)
            y_rand = random.randint(0 + cell_bact, height - cell_bact)
            ret.append(Bact(x_rand, y_rand, ai.change_best_weight(weight[0])))
        return ret