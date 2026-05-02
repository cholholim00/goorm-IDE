import turtle

def draw_tree(branch_len, t):
    # 1. 기본 케이스: 가지 길이가 너무 짧아지면 중단
    if branch_len > 5:
        # 나뭇가지 그리기
        t.forward(branch_len)
        
        # 오른쪽으로 20도 회전하여 오른쪽 가지 그리기 (재귀)
        t.right(20)
        draw_tree(branch_len - 15, t)
        
        # 왼쪽으로 40도 회전하여 왼쪽 가지 그리기 (재귀)
        # (오른쪽으로 20도 갔으므로 왼쪽으로 40도 가야 반대편 20도가 됨)
        t.left(40)
        draw_tree(branch_len - 15, t)
        
        # 원래 각도로 복귀 (오른쪽으로 20도 회전)
        t.right(20)
        
        # 원래 위치로 후진하여 복귀 (이게 핵심!)
        t.backward(branch_len)

def main():
    t = turtle.Turtle()
    my_win = turtle.Screen()
    
    t.left(90)      # 위쪽 방향을 향하게 설정
    t.up()
    t.backward(100) # 아래쪽에서 시작하도록 이동
    t.down()
    t.color("green")
    t.speed(0)      # 가장 빠른 속도
    
    draw_tree(75, t) # 시작 길이 75로 트리 그리기
    my_win.exitonclick()

if __name__ == "__main__":
    main()