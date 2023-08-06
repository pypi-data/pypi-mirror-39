# circulartape

It's a node-oriented circular linked list implementation.

## Example

    from circulartape import Tape

    one = Tape("one")  # one.to_list() == ["one"]
    two = one.insert("two")  # one.to_list() == ["one", "two"]
    three = two.insert("three")  # one.to_list() == ["one", "two", "three"]

    two.remove()  # one.to_list() == ["one", "three"]

    # You can build a long list and seek through it n nodes at a time:
    one = Tape(1)
    current = one
    for i in range(2, 100):
        current = current.insert(i)

    one.seek(30).data  # => 31

    # Use negative values to seek backwards.
