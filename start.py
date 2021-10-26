from pca9685_driver import Device
import math
import time


l_pin = [1, 7, 4]
r_pin = [2, 8, 5]
pwm_pin = [3, 6, 9]
kecepatan = 500



# ------------- Mencari device PCA9685 yang terhubung ke I2C BUS ------------- #
# Mendapatkan I2C yang ada.
i2c_devs = Device.get_i2c_bus_numbers()
print("\nDevice /dev/i2c-* yang ditemukan:\n{}\n".format(i2c_devs))

# Inisiasi variabel working_devs sebagai list()
# untuk menampung device yang terhubung ke PCA9685.
working_devs = list()

# Mencari device PCA9685 yang terhubung.
print("Mencari tahu device /dev/i2c-* mana yang terhubung ke PCA9685...")
for dev in i2c_devs:
    try:
        pca9685 = Device(0x40,dev)
        pca9685.set_pwm(5, 2047)
        pca9685.set_pwm_frequency(1000)
        print("Device {} terhubung dengan PCA9685!".format(dev))
        working_devs.append(dev)
    except:
        print("Device {} tidak terhubung dengan PCA9685.".format(dev))

# Jika tidak ada PCA9685 yang terhubung, exit.
if not working_devs:
    print("\nTidak ada PCA9685 yang terhubung ke device I2C.\n")
    exit()

# Pilih PCA9685 yang terhubung di working_devs. Misalnya yang pertama.
print("Mengonfigurasi PCA9685 yang terhubung ke device /dev/i2c-{}.".format(working_devs[0]))
pca9685 = Device(0x40, working_devs[0])
# ---------------------------------------------------------------------------- #



# ---------------------- Fungsi untuk menggerakkan motor --------------------- #
def motor(pwm, motor):

    if (pwm < 0):
        pca9685.set_pwm(pwm_pin[motor], int(abs(pwm)))
        pca9685.set_pwm(r_pin[motor], 4095)
        pca9685.set_pwm(l_pin[motor], 0)

    else:
        pca9685.set_pwm(pwm_pin[motor], int(abs(pwm)))
        pca9685.set_pwm(r_pin[motor], 0)
        pca9685.set_pwm(l_pin[motor], 4095)
# ---------------------------------------------------------------------------- #



# ----------------------------- Fungsi kinematis ----------------------------- #
def kinematis(x, y, speed):

    m = []

    m.append(x*(-0.5)*speed - y*(math.sqrt(3)/2)*speed * 0.33)
    m.append(x*(-0.5)*speed + y*(math.sqrt(3)/2)*speed * 0.33)
    m.append(x*speed)

    print(m)

    for i in range(3):
        motor(m[i], i)
# ---------------------------------------------------------------------------- #



# ------------------------------- Main program ------------------------------- #
while True:
    # x:0, y:1 | Robot bergerak maju ke depan.
    kinematis(1, 0, kecepatan)
    time.sleep(1)

    # x:1, y:1 | Robot bergerak menyerong ke kanan depan.
    kinematis(1, 1, kecepatan)
    time.sleep(1)

    # x:1, y:0 | Robot bergerak ke kanan.
    kinematis(1, 0, kecepatan)
    time.sleep(1)

    # x:1, y:-1 | Robot bergerak menyerong ke kanan belakang.
    kinematis(1, -1, kecepatan)
    time.sleep(1)

    # x:0, y:-1 | Robot bergerak mundur ke belakang.
    kinematis(0, -1, kecepatan)
    time.sleep(1)

    # x:-1, y:-1 | Robot bergerak menyerong ke kiri belakang.
    kinematis(-1, -1, kecepatan)
    time.sleep(1)

    # x:-1, y:0 | Robot bergerak ke kiri.
    kinematis(-1, 0, kecepatan)
    time.sleep(1)

    # x:-1, y:1 | Robot bergerak menyerong ke kiri depan.
    kinematis(-1, 1, kecepatan)
    time.sleep(1)
# ---------------------------------------------------------------------------- #