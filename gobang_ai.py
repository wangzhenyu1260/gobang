#!/usr/bin/python
# -*- coding: UTF-8 -*-
from consts import *

next_point = [0, 0]  # AI next step

ratio = 1  # Offensive coefficient. Greater than 1 offensive, less than 1 defensive
DEPTH = 1  # Search depth.It can only be odd.

# Chess type evaluation score
shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]


class GobangAI(object):
    def __init__(self, gobang, state):
        self.__gobang = gobang
        self.__currentPieceState = state

    def one_step(self):
        # ai next point
        i, j = self.ai()
        if not i is None and not j is None:
            # There are already pieces on the chessboard.
            if self.__gobang.get_chessboard_state(i, j) != ChessboardState.EMPTY:
                return False
            else:
                self.__gobang.set_chessboard_state(i, j, self.__currentPieceState)
                list1.append((i, j))
                list3.append((i, j))
                return True
        return False

    def ai(self):
        global cut_count  # count prune
        cut_count = 0
        global search_count  # count search
        search_count = 0
        self.negamax(True, DEPTH, -99999999, 99999999)
        print("Prune count: " + str(cut_count))
        print("Search count: " + str(search_count))
        return next_point[0], next_point[1]

    # Minimax & Alpha-Beta Pruning
    def negamax(self, is_ai, depth, alpha, beta):
        # game over | | Whether the recursive depth of exploration reaches the boundary
        if self.game_win(list1) or self.game_win(list2) or depth == 0:
            return self.evaluation(is_ai)
        blank_list = list(set(list_all).difference(set(list3)))
        self.order(blank_list)  # Search order sort  Improve pruning efficiency
        # Evaluate each candidate step
        for next_step in blank_list:

            global search_count
            search_count += 1

            # If there is no adjacent child in the position, then do not evaluate, reduce computational cost
            if not self.has_neightnor(next_step):
                continue

            if is_ai:
                list1.append(next_step)
            else:
                list2.append(next_step)
            list3.append(next_step)

            value = -self.negamax(not is_ai, depth - 1, -beta, -alpha)
            if is_ai:
                list1.remove(next_step)
            else:
                list2.remove(next_step)
            list3.remove(next_step)

            if value > alpha:
                print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
                print(list3)
                if depth == DEPTH:
                    next_point[0] = next_step[0]
                    next_point[1] = next_step[1]
                # Alpha-Beta Pruning
                if value >= beta:
                    global cut_count
                    cut_count += 1
                    return beta
                alpha = value
        return alpha

    #  The location of the neighbors from the last drop is most likely the best
    def order(self, blank_list):
        last_pt = list3[-1]
        for item in blank_list:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                        blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                        blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))

    def has_neightnor(self, pt):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (pt[0] + i, pt[1] + j) in list3:
                    return True
        return False

    # Evaluation function
    def evaluation(self, is_ai):
        total_score = 0

        if is_ai:
            my_list = list1
            enemy_list = list2
        else:
            my_list = list2
            enemy_list = list1

        # Count AI score
        score_all_arr = []  # The position of the score shape; if there is an intersection, the score doubles
        my_score = 0
        for pt in my_list:
            m = pt[0]
            n = pt[1]
            my_score += self.cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
            my_score += self.cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
            my_score += self.cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
            my_score += self.cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

        #  Count the human's score, and subtract
        score_all_arr_enemy = []
        enemy_score = 0
        for pt in enemy_list:
            m = pt[0]
            n = pt[1]
            enemy_score += self.cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
            enemy_score += self.cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
            enemy_score += self.cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
            enemy_score += self.cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

        total_score = my_score - enemy_score * ratio * 0.1

        return total_score

    # Calculate the score in each direction
    def cal_score(self, m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
        add_score = 0  # add score
        # In one direction, only the largest score item is taken
        max_score_shape = (0, None)

        # If in this direction, the point already has a score shape, no double counting
        for item in score_all_arr:
            for pt in item[1]:
                if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                    return 0

        # Cycle through the score shape in the left and right direction of the drop point
        for offset in range(-5, 1):
            # offset = -2
            pos = []
            for i in range(0, 6):
                if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                    pos.append(2)
                elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                    pos.append(1)
                else:
                    pos.append(0)
            tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
            tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

            for (score, shape) in shape_score:
                if tmp_shap5 == shape or tmp_shap6 == shape:
                    if tmp_shap5 == (1, 1, 1, 1, 1):
                        print('---------------------------')
                    if score > max_score_shape[0]:
                        max_score_shape = (score, ((m + (0 + offset) * x_decrict, n + (0 + offset) * y_derice),
                                                   (m + (1 + offset) * x_decrict, n + (1 + offset) * y_derice),
                                                   (m + (2 + offset) * x_decrict, n + (2 + offset) * y_derice),
                                                   (m + (3 + offset) * x_decrict, n + (3 + offset) * y_derice),
                                                   (m + (4 + offset) * x_decrict, n + (4 + offset) * y_derice)),
                                           (x_decrict, y_derice))

        # Calculate the intersection of two shapes, such as two 3 live intersections
        if max_score_shape[1] is not None:
            for item in score_all_arr:
                for pt1 in item[1]:
                    for pt2 in max_score_shape[1]:
                        if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                            add_score += item[0] + max_score_shape[0]

            score_all_arr.append(max_score_shape)

        return add_score + max_score_shape[0]

    def game_win(self, list):
        for m in range(COLUMN):
            for n in range(ROW):

                if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                        m, n + 3) in list and (m, n + 4) in list:
                    return True
                elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                        m + 3, n) in list and (m + 4, n) in list:
                    return True
                elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                        m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                    return True
                elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                        m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                    return True
        return False
