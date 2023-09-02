import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_directory = os.getcwd()
edge_driver_path = os.path.join(current_directory, 'msedgedriver.exe')

edge_service = EdgeService(edge_driver_path)

root = tk.Tk()
root.withdraw()

winName = 'QR Code detection in OpenCV'
cv2.namedWindow(winName, cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow(winName, 800, 600)

cap = cv2.VideoCapture(0)
qcd = cv2.QRCodeDetector()
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
flag = True

while True:
    ret, frame = cap.read()

    if ret:
        ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)

        if ret_qr:
            for s, p in zip(decoded_info, points):
                if not s:
                    color = (0, 0, 255)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, thickness=2)
                else:
                    color = (0, 255, 0)
                    cv2.putText(frame, "Decoded Data: {}".format(s), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, thickness=2)
                    cv2.imshow(winName, frame)
                    response = messagebox.askyesno("Webpages discovered", "Do you want to open the webpage?")
                    if response:
                        web_url = s
                        cap.release()
                        cv2.destroyAllWindows()
                        driver = webdriver.Edge(service=edge_service)
                        driver.maximize_window()
                        driver.get(web_url)
                        try:
                            WebDriverWait(driver, float('inf')).until(
                                EC.title_is("Closed Page Title")
                            )
                        except:
                            driver.quit()
                            endresponse = messagebox.askyesno("Prompt", "Do you want to scan the code again?")
                            if endresponse:
                                background_color = (64, 64, 64)
                                frame = np.full((600, 800, 3), background_color, dtype=np.uint8)
                                cap.release()
                                cv2.destroyAllWindows()
                                cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
                                cv2.resizeWindow(winName, 800, 600)
                                cap = cv2.VideoCapture(0)
                                cv2.imshow(winName, frame)
                            else:
                                flag = False
                    else:
                        reresponse = messagebox.askyesno("Prompt", "Do you want to re-scan the code?")
                        if not reresponse:
                            cap.release()
                            cv2.destroyAllWindows()
                            flag = False
        if flag:
            cv2.imshow(winName, frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or cv2.getWindowProperty(winName, cv2.WND_PROP_VISIBLE) < 1.0:
        break
