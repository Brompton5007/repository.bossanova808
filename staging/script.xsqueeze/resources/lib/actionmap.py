################################################################################
# MAP OF ACTION NAMES TO ID NUMBERS
# MAP OF XBMC ACTION NAMES TO SQUEEZEBOX ACTION STRINGS

#FROM https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h

def swap_dictionary(original_dict):
   return dict([(v, k) for (k, v) in original_dict.iteritems()])

ACTION_CODES = {

                'ACTION_NONE'             :0,
                'ACTION_MOVE_LEFT'        :1,
                'ACTION_MOVE_RIGHT'       :2,
                'ACTION_MOVE_UP'          :3,
                'ACTION_MOVE_DOWN'        :4,
                'ACTION_PAGE_UP'          :5,
                'ACTION_PAGE_DOWN'        :6,
                'ACTION_SELECT_ITEM'      :7,
                'ACTION_HIGHLIGHT_ITEM'   :8,
                'ACTION_PARENT_DIR'       :9,
                'ACTION_PREVIOUS_MENU'    :10,
                'ACTION_SHOW_INFO'        :11,
                'ACTION_PAUSE'            :12,
                'ACTION_STOP'             :13,
                'ACTION_NEXT_ITEM'        :14,
                'ACTION_PREV_ITEM'        :15,
                'ACTION_FORWARD'          :16,
                'ACTION_REWIND'           :17,
                'REMOTE_0'                :58,
                'REMOTE_1'                :59,
                'REMOTE_2'                :60,
                'REMOTE_3'                :61,
                'REMOTE_4'                :62,
                'REMOTE_5'                :63,
                'REMOTE_6'                :64,
                'REMOTE_7'                :65,
                'REMOTE_8'                :66,
                'REMOTE_9'                :67,
                'ACTION_VOLUME_UP'        :88,
                'ACTION_VOLUME_DOWN'      :89,
                'ACTION_MUTE'             :91,
                'ACTION_JUMP_SMS2'        :142,
                'ACTION_JUMP_SMS3'        :143,
                'ACTION_JUMP_SMS4'        :144,
                'ACTION_JUMP_SMS5'        :145,
                'ACTION_JUMP_SMS6'        :146,
                'ACTION_JUMP_SMS7'        :147,
                'ACTION_JUMP_SMS8'        :148,
                'ACTION_JUMP_SMS9'        :149,

}

SQUEEZE_CODES = {
                'ACTION_NONE'             :'',
                'ACTION_MOVE_LEFT'        :'arrow_left',
                'ACTION_MOVE_RIGHT'       :'arrow_right',
                'ACTION_MOVE_UP'          :'arrow_up',
                'ACTION_MOVE_DOWN'        :'arrow_down',
                'ACTION_PAGE_UP'          :'',
                'ACTION_PAGE_DOWN'        :'',
                'ACTION_SELECT_ITEM'      :'play.single',
                'ACTION_HIGHLIGHT_ITEM'   :'',
                'ACTION_PARENT_DIR'       :'arrow_left',
                'ACTION_PREVIOUS_MENU'    :'arrow_left',
                'ACTION_SHOW_INFO'        :'',
                'ACTION_PAUSE'            :'pause.single',
                'ACTION_STOP'             :'stop',
                'ACTION_NEXT_ITEM'        :'fwd.single',
                'ACTION_PREV_ITEM'        :'rew.single',
                'ACTION_FORWARD'          :'fwd.hold',
                'ACTION_REWIND'           :'rew.hold',
                'REMOTE_0'                :'0',
                'REMOTE_1'                :'1',
                'REMOTE_2'                :'2',
                'REMOTE_3'                :'3',
                'REMOTE_4'                :'4',
                'REMOTE_5'                :'5',
                'REMOTE_6'                :'6',
                'REMOTE_7'                :'7',
                'REMOTE_8'                :'8',
                'REMOTE_9'                :'9',
                'ACTION_VOLUME_UP'        :'volup',
                'ACTION_VOLUME_DOWN'      :'voldown',
                'ACTION_MUTE'             :'muting',
                'ACTION_JUMP_SMS2'        :'2',
                'ACTION_JUMP_SMS3'        :'3',
                'ACTION_JUMP_SMS4'        :'4',
                'ACTION_JUMP_SMS5'        :'5',
                'ACTION_JUMP_SMS6'        :'6',
                'ACTION_JUMP_SMS7'        :'7',
                'ACTION_JUMP_SMS8'        :'8',
                'ACTION_JUMP_SMS9'        :'9',

}

ACTION_NAMES = swap_dictionary(ACTION_CODES)
