import socket


class HDMIMatrix:
    # Define mapping dictionary
    IO_DICT = {
        0: {
            0: 'a09',
            1: 'a19',
            2: 'a17',
            3: 'a50',
            4: 'a5E',
            5: 'a47',
            6: 'a18',
            7: 'a0A'
        },
        1: {
            0: 'a1D',
            1: 'a1B',
            2: 'a12',
            3: 'a55',
            4: 'a06',
            5: 'a07',
            6: 'a44',
            7: 'a1E'
        },
        2: {
            0: 'a1F',
            1: 'a11',
            2: 'a59',
            3: 'a48',
            4: 'a05',
            5: 'a40',
            6: 'a0F',
            7: 'a0E'
        },
        3: {
            0: 'a0D',
            1: 'a15',
            2: 'a08',
            3: 'a4A',
            4: 'a03',
            5: 'a02',
            6: 'a51',
            7: 'a1A'
        }
    }

    def __init__(self, hostname, zero_index=True):
        self.hostname = hostname
        self._zero_index = zero_index
        self._input_num = 4
        self._output_num = 8
        self._socket = None
        self._socket_connected = False

    # Connect socket
    def connect(self):
        # If already connected, do nothing
        if not self._socket_connected:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.hostname, 23))
            self._socket_connected = True
            return True

    # Map an input to an output (must have connected first)
    def map_io(self, output, input):
        if not self._socket_connected:
            raise Exception('You must connect to the device before using any non-simple functions.')

        i, o = self._check_values(input, output)  # Check input and output values
        if self._zero_index:
            self._socket.send(HDMIMatrix.IO_DICT[i][o].encode())
        else:
            self._socket.send(HDMIMatrix.IO_DICT[i-1][o-1].encode())
        r = self._socket.recv(1024).decode().strip().replace(chr(0), '')
        if self._zero_index:
            return int(r[1]) == output + 1 and int(r[2]) == input
        else:
            return int(r[1]) == output and int(r[2]) == input - 1

    # Quick map IO, handles socket connect and disconnect
    def simple_map_io(self, output, input):
        if not self._socket_connected:
            self.connect()
            r = self.map_io(output, input)
            self.disconnect()
            return r
        else:
            raise Exception("Can't use simple_map_io if connecting manually.")

    # Get the input number a particular output is mapped to
    def get_output(self, output):
        try:
            if self._zero_index:
                return self.get_outputs()[output]
            else:
                return self.get_outputs()[output-1]
        except KeyError:
            raise ValueError('Specified output must be in range.') from None

    # Get all output mappings as dict
    def get_outputs(self):
        if not self._socket_connected:
            raise Exception('You must connect to the device before using any non-simple functions.')

        self._socket.send('Bc'.encode())
        o = self._socket.recv(1024).decode().strip().replace('s', '')
        d = {}
        for i in range(0, self._output_num):
            if self._zero_index:
                d[i] = int(o[i])
            else:
                d[i] = int(o[i]) + 1
        return d

    # Quick get output mappings, handles socket connect and disconnect
    def simple_get_outputs(self):
        if not self._socket_connected:
            self.connect()
            o = self.get_outputs()
            self.disconnect()
            return o
        else:
            raise Exception("Can't use simple_get_inputs if connecting manually.")

    # Quick get output mapping, handles socket connect and disconnect
    def simple_get_output(self, output):
        if not self._socket_connected:
            self.connect()
            o = self.get_output(output)
            self.disconnect()
            return o
        else:
            raise Exception("Can't use simple_get_input if connecting manually.")

    # Disconnect from socket
    def disconnect(self):
        if self._socket_connected:
            self._socket.close()
            self._socket = None
            self._socket_connected = False

    def _check_values(self, input, output):
        try:
            i = int(input)
            o = int(output)
        except ValueError:
            raise ValueError('Input and output indexes must be numbers.') from None

        if self._zero_index:
            if i < 0 or i >= self._input_num:
                raise ValueError('Input index must be within the range of the matrix IO.')
            if o < 0 or o >= self._output_num:
                raise ValueError('Output index must be within the range of the matrix IO.')
        else:
            if i < 1 or i > self._input_num:
                raise ValueError('Input index must be within the range of the matrix IO.')
            if o < 1 or o > self._output_num:
                raise ValueError('Output index must be within the range of the matrix IO.')

        return i, o
