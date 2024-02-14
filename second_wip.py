class qLearning():
    # get game state
    def game_state(self, paddle_one_y_pos, paddle_two_y_pos, ball_x, ball_y, p1_score, p2_score):
        current_state = (paddle_one_y_pos, paddle_two_y_pos, ball_x, ball_y, p1_score, p2_score)
        return current_state