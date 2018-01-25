# Python API for an HDanywhere 4x8 (TTHA428MC) HDMI Matrix #

A Python API for getting and setting inputs on an HDanywhere 4x8 matrix.
Communicates with the matrix over the network to port 23 on the device which is a Telnet control interface.

See [this blog post](https://blog.nyanlabs.com/hdanywhere-4x8-matrix/) for my investigation into the device - given it's nowhere to be found on Google.

## Usage ##

### Setup ###

Clone `hdmi_matrix.py` into your project.

```
$ wget https://raw.githubusercontent.com/Jamie-/hdmi-matrix-api/master/hdmi_matrix.py
```

Create an `HDMIMatrix` object.

```python
m = HDMIMatrix('hostname')
```

By default, all the inputs and outputs are zero-indexed, but you can easily change this as so.

```python
m = HDMIMatrix('hostname', zero_index=False)
```


### Simple Control ###

To control the device with the smallest amount of effort you can change the input as follows:

```python
m.simple_map_io(output_num, input_num)
```

Equally you can get an indexed dictionary of the current output mappings with:

```python
m.simple_get_outputs()
```

Which returns like so:

```
{0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
```

Or the mapping of a single output with

```python
m.simple_get_output(output_num)
```

### Finer Control ###

The downsides to the simple control is the process of connecting and disconnecting to the device can get a little too much for it and you will have to rate limit yourself.
Otherwise the matrix get's rather unhappy and looses connection.

In that case, you'll want to use finer control where you connect, run your commands, then disconnect when done.
First, you'll need to connect:

```python
m.connect()
```

Then you can issue commands like in simple control, just with the `simple_` omitted:

```python
m.map_io(output_num, input_num)
m.get_outputs()
m.get_output(output_num)
```

Finally, when done, remember to disconnect:

```python
m.disconnect()
```
