# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2024 Daniel Rodriguez

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from typing import Optional, List, Literal
import bittensor as bt

# ---- miner ----
# Example usage:
#   def dummy( synapse: Dummy ) -> Dummy:
#       synapse.dummy_output = synapse.dummy_input + 1
#       return synapse
#   axon = bt.axon().attach( dummy ).serve(netuid=...).start()

# ---- validator ---
# Example usage:
#   dendrite = bt.dendrite()
#   dummy_output = dendrite.query( Dummy( dummy_input = 1 ) )
#   assert dummy_output == 2


class RedditProtocol(bt.Synapse):
    """
    A simple protocol representation which uses bt.Synapse as its base.
    This protocol helps in handling request and response communication between
    the miner and the validator.

    Attributes:
    - input: An integer value representing the input request sent by the validator.
    - output: An optional integer value which, when filled, represents the response from the miner.
    """

    # Required request input, filled by sending dendrite caller.
    subreddit: str

    # Optional request input, filled by sending dendrite caller.
    sort_by: Optional[Literal['hot', 'new', 'rising', 'random_rising']] = 'new'
    limit: Optional[int] = 10


    # Optional request output, filled by recieving axon.
    output: Optional[List[dict]] = None

    def deserialize(self) -> List[dict]:
        """
        Deserialize the output. This method retrieves the response from
        the miner in the form of output, deserializes it and returns it
        as the output of the dendrite.query() call.

        Returns:
        - List[dict]: The deserialized response.

        Example:
        Assuming a RedditProtocol instance has a output value of "test":
        >>> instance = RedditProtocol(subreddit="test")
        >>> instance.output = [{"foo": "bar"}]
        >>> instance.deserialize()
        [{"foo": "bar"}]
        """
        return self.output
