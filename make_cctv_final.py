import cv2
import datetime

cap = cv2.VideoCapture(0)  # 카메라 열기
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정

# 파일 이름을 현재 시간으로 지정
now = datetime.datetime.now()
filename = "output_{}.avi".format(now.strftime("%Y%m%d_%H%M%S"))

out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))  # 녹화할 파일 설정

font = cv2.FONT_HERSHEY_SIMPLEX  # 폰트 설정
org = (50, 50)  # 텍스트 위치
fontScale = 1  # 폰트 크기
color = (0, 0, 255)  # 빨간색
thickness = 2  # 선 두께

recording = False  # 녹화 중인지 여부
start_time = None  # 녹화 시작 시간

while cap.isOpened():
    ret, frame = cap.read()  # 프레임 읽기
    
    if ret:
        if recording:
            now = datetime.datetime.now()  # 현재 날짜와 시간 가져오기
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")  # 날짜와 시간을 문자열로 변환
            cv2.putText(frame, "REC", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # REC 글자 출력
            cv2.putText(frame, date_time, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  # 날짜와 시간 출력

            if start_time is not None:
                # 현재 시간에서 녹화 시작 시간을 빼서 경과 시간 계산
                elapsed_time = datetime.datetime.now() - start_time

                # 깜빡이는 빨간색 동그라미 추가
                if int(elapsed_time.total_seconds()) % 2 == 0:  # 1초마다 깜빡임
                    cv2.circle(frame, (30, 30), 10, (0, 0, 255), thickness=-1)
                else:
                    cv2.circle(frame, (30, 30), 10, (0, 0, 0), thickness=-1)

            out.write(frame)  # 프레임 저장

        cv2.imshow('frame', frame)  # 프레임 출력

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # 'q'를 누르면 종료
            break
        elif key == ord('r'):  # 'r'을 누르면 녹화 시작 또는 중지
            recording = not recording
            if recording:
                start_time = datetime.datetime.now()
            else:
                start_time = None
    else:
        break

cap.release()  # 카메라 해제
out.release()  # 파일 닫기
cv2.destroyAllWindows()
