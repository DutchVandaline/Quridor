from board import Board
from random import sample, uniform
from BFS import BFS
import copy

class Player:
    def __init__(self, board, name=''):
        self.pawn = None
        self.board = board
        self.name = name
        self.score = 0

    def set_pawn(self, pawn):
        self.pawn = pawn

    def play(self):
        best_move = None
        best_value = float('-inf') 
        #alpha-beta pruning
        alpha = float('-inf')      #음의 무한대로 초기화
        beta = float('inf')        #양의 무한대로 초기화

        possible_moves = self.get_possible_moves()
        for move in possible_moves:
            new_board = self.apply_move(self.board, move)
            move_value = self.minimax(new_board, depth=3, alpha=alpha, beta=beta, maximizing_player=False)
            if move_value > best_value:
                best_value = move_value
                best_move = move

        if best_move: #최선책이 있다면 움직임
            self.board.move_player(best_move, self.pawn) 
        else: #최선책이 없다면 벽 설치
            threshold = 0.9
            if uniform(0,1) <= threshold: #랜덤 움직임
                pos_dir = self.board.search_direction(self.pawn)
                if len(pos_dir) > 0:
                    dir = sample(pos_dir, 1)[0]
                    self.board.move_player(dir, self.pawn)
            else: #벽설치
                r = sample(range(self.board.rows), 1)[0]
                c = sample(range(self.board.cols), 1)[0]
                d = sample(range(0,2), 1)[0] + 1
                self.wall(r, c, d)

    def minimax(self, board_state, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_finish():
            return self.evaluate_board(board_state)

        if maximizing_player: #미니맥스에서 이익을 최대화 시키는 방식으로 진행
            max_eval = float('-inf')
            for move in self.get_possible_moves():
                new_board_state = self.apply_move(board_state, move)
                eval = self.minimax(new_board_state, depth-1, alpha, beta, False) #재귀적 계산
                max_eval = max(max_eval, eval) #계산값 중 최대를 반영
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves():
                new_board_state = self.apply_move(board_state, move)
                eval = self.minimax(new_board_state, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    #가능한 모든 움직임 분석.
    def get_possible_moves(self):
        possible_moves = []
        for direction in range(1, 10):
            if self.board.move_player(direction, self.pawn):
                possible_moves.append(direction) #만약 valid한 움직임이라면 리스트에 추가, 아니라면 되돌리기(재귀적)
                self.reverse_move(direction)
        return possible_moves

    def apply_move(self, board_state, move):
        new_board = copy.deepcopy(board_state) #deepcopy 개념은 몰라서 찾아봤습니다. 여기서는 보드를 복사
        new_board.move_player(move, self.pawn)
        return new_board

    def reverse_move(self, direction): #valid한 move가 아닐 시 다시 복귀
        if direction == 1:
            reverse_direction = 3
        elif direction == 2:
            reverse_direction = 4
        elif direction == 3:
            reverse_direction = 1
        elif direction == 4:
            reverse_direction = 2
        elif direction == 5:
            reverse_direction = 7
        elif direction == 6:
            reverse_direction = 8
        elif direction == 7:
            reverse_direction = 5
        elif direction == 8:
            reverse_direction = 6
        else:
            reverse_direction = None

        if reverse_direction is not None:
            self.board.move_player(reverse_direction, self.pawn)


    def evaluate_board(self, board_state):
        #board_state를 받아서 현재 위치 저장
        if self.pawn == 1:
            current_position = board_state.pawn[0]
        elif self.pawn == 2:
            current_position = board_state.pawn[1]
        else:
            raise ValueError("Error")

        start = tuple(current_position) #BFS에서 오류가 발생하여 넣은 tuple 함수
        end = (board_state.rows - 1, current_position[1]) #BFS를 사용하기 위한 수정

        path_length = BFS(board_state.maze, start, end)

        if board_state.is_finish():
            return float('inf') if current_position[0] >= board_state.rows - 1 else float('-inf')
        else:
            return -path_length


    def move(self, direction):
        res = self.board.move_player(direction, self.pawn)
        return res

    def wall(self, r, c, direction):
        res = self.board.put_wall(r, c, direction, self.pawn)
        return res