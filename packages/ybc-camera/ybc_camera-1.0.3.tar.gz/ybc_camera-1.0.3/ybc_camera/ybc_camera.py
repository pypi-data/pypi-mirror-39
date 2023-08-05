import cv2
import time
import sys
from ybc_exception import *


def camera(filename=''):
    """
    功能：拍摄一张照片，文件名存储为filename
    :param filename:要存储的文件名
    """
    error_msg = "'filename'"
    if not isinstance(filename, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    if not filename:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    try:
        cap = cv2.VideoCapture(0)
        while 1:
            ret, frame = cap.read()
            cv2.imshow("capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                now = time.localtime()
                if filename == '':
                    filename = str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) + '.jpg'
                cv2.imwrite(filename, frame)
                break
        cap.release()
        cv2.destroyAllWindows()
        return filename
    except Exception as e:
        raise InternalError(e, 'ybc_camera')


def main():
    res = camera()
    print(res)


if __name__ == '__main__':
    main()
