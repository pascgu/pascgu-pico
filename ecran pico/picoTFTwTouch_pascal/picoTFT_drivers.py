import utime as time
import machine

class gt:
    # Configuration information (R/W)
    CONFIG_SIZE = 0xFF - 0x46
    CONFIG_START = 0x8047
    X_OUTPUT_MAX_LOW = 0x8048
    X_OUTPUT_MAX_HIGH = 0x8049
    Y_OUTPUT_MAX_LOW = 0x804A
    Y_OUTPUT_MAX_HIGH = 0x804B
    # Coordinate information
    POINT_INFO = 0x814E
    POINT_1 = 0x814F

class Addr:
    ADDR1 = 0x5D
    ADDR2 = 0x14

class TouchPt:
    def __init__(self, id, x, y, size, t):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.t = t

    def set_from(self, pt):
        self.id = pt.id
        self.x = pt.x
        self.y = pt.y
        self.size = pt.size
        self.t = pt.t
    def clone(self):
        return TouchPt(self.id, self.x, self.y, self.size, self.t)
    
    def __str__(self):
        return f"{{id:{self.id},x:{self.x},y:{self.y},size:{self.size},t:{self.t}}}"

class GT911_picoTFT:
    def __init__(self, sda, scl, interrupt, reset, width, height, rotation=0, use_time=False, freq=100_000):
        self.width = width
        self.height = height
        self.rotation = rotation
        self.address = None
        self.configuration = []
        #self.i2c = machine.I2C(freq=freq, scl=machine.Pin(scl), sda=machine.Pin(sda))
        self.i2c = machine.I2C(0,freq=freq, scl=machine.Pin(scl), sda=machine.Pin(sda)) # PG : ajout id=0
        self.interrupt = machine.Pin(interrupt, machine.Pin.OUT)
        self.reset_pin = machine.Pin(reset, machine.Pin.OUT)

        self.parse_point = self.parse_point_rot0
        if self.rotation==270: self.parse_point = self.parse_point_rot270

        self.use_time = use_time
        self.bytes_0 = bytes([0])
        self.buff_points_len = 0
        self.buff_points:list[TouchPt] = []
        for i in range(16):
            self.buff_points.append(TouchPt(-1,-1,-1,0,0))
    
    def enable_interrupt(self, callback):
        self.interrupt.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)

    def config_offset(self, reg: int):
        return reg - gt.CONFIG_START
    
    def begin(self, address = Addr.ADDR1):
        self.address = address
        self.reset()
        self.configuration = self.read(gt.CONFIG_START, gt.CONFIG_SIZE)
        wl = self.configuration[self.config_offset(gt.X_OUTPUT_MAX_LOW)]
        wh = self.configuration[self.config_offset(gt.X_OUTPUT_MAX_HIGH)]
        hl = self.configuration[self.config_offset(gt.Y_OUTPUT_MAX_LOW)]
        hh = self.configuration[self.config_offset(gt.Y_OUTPUT_MAX_HIGH)]
        self.width = (wh << 8) + wl
        self.height = (hh << 8) + hl

    def reset(self):
        self.interrupt.value(0)
        self.reset_pin.value(0)
        time.sleep_ms(10)
        self.interrupt.value(self.address == Addr.ADDR2)
        time.sleep_ms(1)
        self.reset_pin.value(1)
        time.sleep_ms(5)
        self.interrupt.value(0)
        time.sleep_ms(50)
        self.interrupt.init(mode=machine.Pin.IN)
        time.sleep_ms(50)

    def get_points(self) -> None:
        info = self.read(gt.POINT_INFO, 1)[0]
        ready = bool((info >> 7) & 1)
        # large_touch = bool((info >> 6) & 1)
        touch_count = info & 0xF
        if ready and touch_count > 0:
            ticks_us = 0
            if self.use_time: ticks_us = time.ticks_us()
            for i in range(touch_count):
                data = self.read(gt.POINT_1 + (i * 8), 7)
                self.parse_point(i, data, ticks_us)
        self.write(gt.POINT_INFO, self.bytes_0)
        self.buff_points_len = touch_count
    
    def remove_point(self,i):
        if i < self.buff_points_len-1:
            self.buff_points[i].set_from(self.buff_points[i+1])
        self.buff_points_len -= 1

    def parse_point_rot0(self, i, data, ticks_us):
        self.buff_points[i].id = data[0] # track_id
        self.buff_points[i].x = data[1] + (data[2] << 8)
        self.buff_points[i].y = data[3] + (data[4] << 8)
        self.buff_points[i].size = data[5] + (data[6] << 8)
        self.buff_points[i].t = ticks_us
        
    def parse_point_rot270(self, i, data, ticks_us):
        self.buff_points[i].id = data[0] # track_id
        self.buff_points[i].x = data[3] + (data[4] << 8)
        self.buff_points[i].y = self.width - (data[1] + (data[2] << 8))
        self.buff_points[i].size = data[5] + (data[6] << 8)
        self.buff_points[i].t = ticks_us

    def write(self, reg: int, value: bytes):
        self.i2c.writeto_mem(self.address, reg, value, addrsize=16)

    def read(self, reg: int, length: int):
        return self.i2c.readfrom_mem(self.address, reg, length, addrsize=16)

