"""
author: Khoa Le
email: lenguyenkhoa1988@gmail.com

The Raft consensus algorithm.
Implementation follows the paper
Resources: https://raft.github.io/
"""
import time, random, os, json, threading, copy
from chatqhelper.mqtt import MqttClient
from chatqhelper import scheduler
from functools import wraps
from chatqhelper.common import constants


class State():
    """ Base State of Raft state machine
    """
    def __init__(self, machine, timeout, multiplier=2):
        """
        Args:
            - machine: the raft server
            - timeout: the lower timeout in second. used to determine the lower bound of timeout period
            - multiplier: the multiplier of timeout. used to determine the upper bound of timeout period
        """
        self.machine = machine
        self.timeout = timeout
        self.multiplier = multiplier if multiplier >= 1 else 1
        self.easy_log('init with timeout', self.timeout)

    @property
    def current_term(self):
        """shortcut to get current term from machine"""
        return self.machine._current_term
    
    @current_term.setter
    def current_term(self, term):
        """shortcut to set current term of machine """
        self.machine._current_term = term

    def _next_timeout(self):
        """ update the timeout time. the timeout period is defined by a random number better timeout lower and upperbound.
        lower bound timeout is defined when initalizing the state
        upper bound timeout is defined when initalize the state with the multiplier
        """
        self._cur_time = time.time()
        period = random.randint(self.timeout, self.timeout*self.multiplier) / 1000
        self._timeout_time =  self._cur_time + period
        return self._timeout_time

    def on_message(self, message):
        """called when there's a message
        this is where common behavior should be called regardless the message type
        """
        # self.easy_log('on message')
        term = message.payload['term']
        # If RPC request or response contains term T > currentTerm: set currentTerm = T, convert to follower 
        if term > self.current_term:
            self.current_term = term
            self.machine.state = self.machine.follower
            return

    def on_append_entries(self, message):
        """called when there is an append entries request"""
        # self.easy_log('on append entries', message.payload)
        pass
    
    def on_append_replied(self, message):
        """called when the append entried request is replied (for leader)"""
        # self.easy_log('on append replied', message.payload)
        pass
    
    def on_request_vote(self, message):
        """called when there's a vote request"""
        # self.easy_log('on request vote', message.payload)
        pass

    def on_vote_received(self, message):
        """called when a vote request is replied (for candidate)"""
        # self.easy_log('on vote received', message.payload)
        pass
    
    def on_enter(self):
        """called when entering a new state upon state change"""
        self.easy_log('enter')
        pass

    def on_exit(self):
        """called when exiting an old state upon state change"""
        self.easy_log('exit')
        pass

    def on_timeout(self):
        """called when the timeout reaches"""
        self.easy_log('timeout')
        pass
    
    def easy_log(self, *messages):
        """easy log"""
        print('[{}]'.format(self.__class__.__name__), messages)
        pass

    def on_command(self, message):
        self.easy_log('on command')
        pass

    @property
    def current_term(self):
        return self.machine._current_term
    
    @current_term.setter
    def current_term(self, term):
        self.machine._current_term = term

class Leader(State):
    def __init__(self, machine, timeout, multiplier=1):
        # timeout should be less than regular timeout for hearbeat
        # multiplier should be 1 for the upper bound
        super(Leader, self).__init__(machine, timeout//4, multiplier)
        self._on_leader = None

    def on_enter(self):
        super(Leader, self).on_enter()
        self._next_timeout()
        self.send_heart_beat()

        # self._next_index = {
        #     'default': len(self.machine._log)
        # }
        # # self._next_index = self.machine._last_log_idx + 1
        # self._match_index = {
        #     'default': 0
        # }

        if self._on_leader: 
            self._on_leader[0](*self._on_leader[1])

        
    def send_heart_beat(self):
        # self.easy_log('send heart beat')
        # self.machine.append_entry()
        heart_beat = {
            'term': self.machine._current_term, 
            # 'prev_log_idx': 0,
            # 'prev_log_term': 0,
            'entries': [],
            # 'leader_commit_idx': self.machine._commit_index,
            'correlation_id': self.machine._id
        }
        self.machine._mqtt_client.publish(self.machine._entry_topic, json.dumps(heart_beat))

    def on_timeout(self):
        # super(Leader, self).on_timeout()
        self._next_timeout()
        self.send_heart_beat()
    
    # def on_append_replied(self, message):
    #     super(Leader, self).on_append_replied(message)
    #     success = message.payload['success']
    #     if not success: 
    #         self.easy_log('--------HEHEHHE---------')
    #         self.easy_log(message.payload['prev_log_idx'])

    #         prev_log_idx = message.payload['prev_log_idx']
    #         prev_entry = self.machine._log[prev_log_idx]
    #         append_entry = {
    #             'term': self.machine._current_term, 
    #             'prev_log_idx': prev_log_idx,
    #             'prev_log_term': prev_entry['term'],
    #             'entries': [self.machine._log[prev_log_idx:]],
    #             'leader_commit_idx': self.machine._commit_index,
    #             'correlation_id': self.machine._id
    #         }
    #     message.topic = self.machine._entry_topic
    #     self.machine._mqtt_client.reply(message, append_entry)

    def on_command(self, message):
        super(Leader, self).on_command(message)
        # If command received from client: append entry to local log, respond after entry applied to state machine
        entry = {
            'term': self.current_term,
            'data': 'test'
        }
        self.machine._log.append(entry)

        self.machine.append_entry(entry)
    
class Candidate(State):
    def on_enter(self):
        super(Candidate, self).on_enter()
        # start new election upon state enter
        self.start_election()

    def start_election(self):
        # increse current term, vote for self, reset election timer, send 
        self.current_term += 1
        self.easy_log('start new election with terms <{}>'.format(self.current_term))
        self._votes = [self.machine._id]
        self._next_timeout()
        self.machine._vote_for = self.machine._id
        self.machine.request_vote()

    def on_vote_received(self, message):
        super(Candidate, self).on_vote_received(message)

        # only check when vote is granted
        if not message.payload['success']:
            return

        # If votes received from majority of servers: become leader
        sender = message.payload['correlation_id']
        if sender not in self._votes:
            self._votes.append(sender)
            self.machine.response(message, True)
            if len(self._votes) > self.machine._num_member//2:
                self.machine.state = self.machine.leader
            return

    def on_timeout(self):
        super(Candidate, self).on_timeout()
        # If election timeout elapses: start new election
        self.start_election()

    def on_append_entries(self, message):
        # if append entries received form a leader, convert to follower
        super(Candidate, self).on_append_entries(message)
        self.machine.state = self.machine.follower


class Follower(State):
    def on_append_entries(self, message):
        super(Follower, self).on_append_entries(message)
        self._next_timeout()

        # Reply false if term < current_term
        term = message.payload['term']
        if term < self.machine._current_term:
            self.machine.response(False)
            return
        
        # heart beat
        # entries = message.payload['entries']
        # if not entries:
        #     return

        # Reply false if log doesn’t contain an entry at prevLogIndex whose term matches prevLogTerm
        # log = self.machine._log
        # prev_log_idx = message.payload['prev_log_idx']
        # if len(log) < prev_log_idx:
        #     self.easy_log('---------------------------')
        #     message.topic = self.machine._entry_topic
        #     print('>>>>>>>>>', type(message.payload))
        #     self.machine.response(message, False)
        #     return
        
        # # If an existing entry conflicts with a new one (same index but different terms), delete the existing entry and all that follow it
        # entry = log[prev_log_idx]
        # if term != entry['term']:
            # self.machine._log = log[:prev_log_idx]
        
        # # append any new entries not already in the log
        # for e in message.payload['entries']:
        #     log.append(e)
        #     self.machine._log = log
        #     self.easy_log('-------', self.machine._log)

        # If leaderCommit > commitIndex, set commitIndex = min(leaderCommit, index of last new entry)
        # leader_commit_idx = message.payload['leader_commit_idx']
        # if leader_commit_idx > self.machine._commit_index:
        #     self.machine._commit_index = min(leader_commit_idx, len(log) - 1)
        #     self.easy_log('~~~~~~~', self.machine._commit_index)
        # self.on_append_replied(message)

    # def on_append_replied(self, message):
    #     super(Follower, self).on_append_replied(message)

    #     self._next_timeout()

    #     # Reply false if term < current_term
    #     term = message.payload['term']
    #     if term < self.machine._current_term:
    #         self.machine.response(False)
    #         return
        
    #     # heart beat
    #     entries = message.payload['entries']
    #     if not entries:
    #         return

    #     # Reply false if log doesn’t contain an entry at prevLogIndex whose term matches prevLogTerm
    #     log = self.machine._log
    #     prev_log_idx = message.payload['prev_log_idx']
    #     if len(log) < prev_log_idx:
    #         self.easy_log('---------------------------')
    #         message.topic = self.machine._entry_topic
    #         print('>>>>>>>>>', type(message.payload))
    #         self.machine.response(message, False)
    #         return
        
    #     # # If an existing entry conflicts with a new one (same index but different terms), delete the existing entry and all that follow it
    #     # entry = log[prev_log_idx]
    #     # if term != entry['term']:
    #         # self.machine._log = log[:prev_log_idx]
        
    #     # append any new entries not already in the log
    #     for e in message.payload['entries']:
    #         log.append(e)
    #         self.machine._log = log
    #         self.easy_log('-------', self.machine._log)

    #     # If leaderCommit > commitIndex, set commitIndex = min(leaderCommit, index of last new entry)
    #     # leader_commit_idx = message.payload['leader_commit_idx']
    #     # if leader_commit_idx > self.machine._commit_index:
    #     #     self.machine._commit_index = min(leader_commit_idx, len(log) - 1)
    #     #     self.easy_log('~~~~~~~', self.machine._commit_index)


    def on_timeout(self):
        super(Follower, self).on_timeout()
        # If election timeout elapses without receiving AppendEntries from current leader or granting vote to candidate: convert to candidate
        self.machine.state = self.machine.candidate

    def on_enter(self):
        super(Follower, self).on_enter()
        self._next_timeout()
        self.machine._vote_for = None

    def on_request_vote(self, message):
        super(Follower, self).on_request_vote(message)
        self._next_timeout()

        # response to candidate
        term = message.payload['term']
        # Reply false if term < currentTerm
        if term < self.machine._current_term:
            self.machine.response(message, False)
            return

        # If votedFor is null or candidateId, and candidate’s log is at least as up-to-date as receiver’s log, grant vote
        sender = message.payload['correlation_id']
        vote_for = self.machine._vote_for
        if vote_for is None or vote_for == sender:
            self.machine._vote_for = sender
            self.machine.response(message, True)
            return 
    


class Raft():
    """ Raft server using pubsub

    Support:
        - leader election

    Future:
        - log replication
        - membership change

    Testing:
        - coming
    
    Usage:
        - create raft server with default value
            raft = Raft()

        - start raft server
            raft = raft.start()

        - use decorator to define function to execute only when raft server is the leader
            @raft.leader_only
            def test():
                pass
    
    TODO:
        - remove log
        - add support for log replication
    """

    DEFAULT_TIMEOUT_MS = 500
    DEFAULT_NUM_CLUSTER_MEMBERS = 5

    APPEND_ENTRIES_TOPIC = 'raft/{}/append_entries'
    REQUEST_VOTE_TOPIC = 'raft/{}/request_vote'
    COMMAND_TOPIC = 'raft/{}/command'
    REPLICATE_TOPIC = 'raft/{}/replicate'


    def __init__(self, cluster_id=constants.SERVICE_NAME, member_id=constants.HOSTNAME, client=None, timeout=DEFAULT_TIMEOUT_MS, num_members=DEFAULT_NUM_CLUSTER_MEMBERS):
        """ raft server/state-machine
        Args:
            - cluster_id: to identify the raft system
            - member_id: to identify this node
            - client: mqtt client
            - timeout: default timeout for states in miliseconds
            - num_members: the number of member in the cluster. This is important as to decide which number is the majority of vote. default to 5
        """
        # the id to identify the cluster. Each raft cluster will have its own id or namespace to communicate
        self._clus_id = cluster_id
        self._id = member_id if member_id != cluster_id else '-'.join([member_id, str(os.getpid())])
        self._num_member = num_members
        self._is_leader = False

        # two basic command
        self._entry_topic = Raft.APPEND_ENTRIES_TOPIC.format(self._clus_id)
        self._vote_topic = Raft.REQUEST_VOTE_TOPIC.format(self._clus_id)
        self._command_topic = Raft.COMMAND_TOPIC.format(self._clus_id)
        self._replicate_topic = Raft.REPLICATE_TOPIC.format(self._clus_id)

        # pubsub client
        self._mqtt_client = client or MqttClient.create(self.on_mqtt_connect)

        # 3 persist state according to raft paper
        self._current_term = 0
        self._vote_for = None
        self._log = []

        # volatile state on all servers
        self._commit_index = 0
        self._last_applied = 0

        

        # three state of raft
        self.follower = Follower(self, timeout=timeout)
        self.candidate = Candidate(self, timeout=timeout)
        self.leader = Leader(self, timeout=timeout)
        self._state = None
        
        # 
        self._on_replicate_state = None

    def on_mqtt_connect(self, client, userdata, flags, rc):

        print("connected with result code " + str(rc))
        # channels to broadcast request
        self._mqtt_client.message_callback_add(
            self._entry_topic, self.on_append_entries
        )
        self._mqtt_client.message_callback_add(
            self._vote_topic, self.on_request_vote
        )
        self._mqtt_client.message_callback_add(
            self._command_topic, self.on_command
        )
        self._mqtt_client.message_callback_add(
            self._replicate_topic, self.on_replicate
        )

        # channels to communicate directly with others
        self._mqtt_client.message_callback_add(
            self._entry_topic + '/reply-to/{}'.format(self._id), self.on_append_replied
        )
        self._mqtt_client.message_callback_add(
            self._vote_topic + '/reply-to/{}'.format(self._id), self.on_vote_received
        )

    def on_append_entries(self, client, message):
        sender = message.payload['correlation_id']
        if sender == self._id:
            return
        self.state.on_message(message)
        self.state.on_append_entries(message)

    def on_request_vote(self, client, message):
        sender = message.payload['correlation_id']
        if sender == self._id:
            return
        self.state.on_message(message)
        self.state.on_request_vote(message)
   
    def on_append_replied(self, client, message):
        print('----------WTFFFF---------')
        self.state.on_message(message)
        self.state.on_append_replied(message)

    def on_vote_received(self, client, message):
        self.state.on_message(message)
        self.state.on_vote_received(message)

    def on_command(self, client, message):
        self.state.on_command(message)
    
    def on_replicate(self, client, message):
        sender = message.payload.pop('correlation_id')
        if sender == self._id:
            return
        
        if self._on_replicate_state:
            self._on_replicate_state(message.payload)
    
    @property
    def on_replicate_state(self):
        return self._on_replicate_state

    @on_replicate_state.setter
    def on_replicate_state(self, func):
        self._on_replicate_state = func

    def start(self):
        self.state = self.follower
        scheduler.every(0.1).seconds.do(self.timeout_check)
        scheduler.loop_start(0.05)
        self._mqtt_client.loop_start()
        return self

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        """state setter"""
        if state != self._state:
            if self._state:
                self._state.on_exit()
            self._state = state
            self._state.on_enter()
            self._is_leader = state == self.leader
    
    @property
    def on_leader(self):
        return self.leader._on_leader

    @on_leader.setter
    def on_leader(self, on_leader):
        if not isinstance(on_leader, list) and not isinstance(on_leader, tuple):
            on_leader = (on_leader, ())
        assert len(on_leader) == 2, "wrong assignment. must be a tuple (function, (args))"
        self.leader._on_leader = on_leader
        return self

    def timeout_check(self):
        if self.state._timeout_time - time.time() < 0:
            self.state.on_timeout()
        
    def on_message(self, client, message):
        self.state.on_message(message)

    # TODO: move request to state
    def append_entry(self, entry=None):
        """NOTE: should be used by Leader only"""
        # # prev_log = self._log[]
        # next_index = self.leader._next_index.get('default') - 1
        # prev_index = next_index - 1
        # print('>>>>>>>>>>>>>', len(self._log), prev_index)
        # prev_entry = self._log[prev_index] if len(self._log) > prev_index else {'term': self._current_term}
        # print('>>>>>>>>>>', entry)
        # print('<<<<<<<<<<', self._log)
        prev_index = 0
        prev_entry = {'term': self._current_term}
        if entry:
            prev_index = len(self._log) - 1
            prev_entry = self._log[prev_index] if prev_index > 0 else prev_entry
            print('~~~~~~~~~~~~', prev_index, prev_entry)
        message = {
            'term': self._current_term, 
            'prev_log_idx': prev_index,
            'prev_log_term': prev_entry['term'],
            'entries': [] if not entry else [entry],
            'leader_commit_idx': self._commit_index,
            'correlation_id': self._id
        }
        self._mqtt_client.publish(self._entry_topic, json.dumps(message), qos=1)

    def request_vote(self):
        message = {
            'correlation_id': self._id,
            'term': self._current_term,
            'last_log_idx': 0,
            'last_log_term': 0,
        }
        self._mqtt_client.publish(self._vote_topic, json.dumps(message), qos=1)

    def response(self, message, success):
        reply_message = copy.deepcopy(message.payload)
        reply_message.update({
            'correlation_id': self._id,
            'term': self._current_term,
            'success': success
            }
        )
        self._mqtt_client.reply(message, reply_message, qos=1, log_response=True)
    
    def leader_only(self, function):
        """decorator to pause execution on node not being a leader"""
        @wraps(function)
        def callback(*args, **kwargs):
            if self._is_leader: return function(*args, **kwargs)
        return callback
    
    def replicate_state(self, state):
        if not self._is_leader:
            return
        assert isinstance(state, dict), "state has to be a dictionary"
        if 'correlation_id' not in state:
            state['correlation_id'] = self._id
        self._mqtt_client.publish(self._replicate_topic, json.dumps(state))
    

if __name__ == "__main__":
    # quick testing
    raft = Raft(num_members=3, timeout=3000).start()
    @raft.leader_only
    def test():
        x = random.randint(5, 15)
        print('.'*x + ' '*(15-x), end='\r')

    def on_replicate_state(state):
        print('hohohohoho', state)
    
    raft.on_replicate_state = on_replicate_state

    print('---------------------------------')
    while True:
        time.sleep(5)
        raft.replicate_state({'a':'b'})
    
