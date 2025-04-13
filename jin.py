# sgpt --code "translate american sign language signing video to english textual paragraphs"
import cv2
import mediapipe as mp
import mediapipe.python.solutions.drawing_styles as ds
import typing
import numpy as np
from queue import Queue
import time
from collections import namedtuple
import sys
import socketio
import random

# Create a Socket.IO client instance
sio = socketio.Client()

# Define event handlers
@sio.event
def connect():
    print("Connection established")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def message(data):
    print(f"Message received: {data}")

# Custom event handler
#@sio.on('custom_event')
#def on_custom_event(data):
#    print(f"Custom event received: {data}")
#    # Respond to the custom event
#    sio.emit('client_response', {'response': 'Received your custom event!'})


mp_hands = mp.solutions.hands.HandLandmark
poselm = mp.solutions.pose.PoseLandmark

hand = [[mp_hands.WRIST, "WRIST", "radiocarpal"],
[mp_hands.THUMB_CMC, "THUMB_CMC", "carpometacarpal_1"],
[mp_hands.THUMB_MCP, "THUMB_MCP", "metacarpophalangeal_1"],
[mp_hands.THUMB_IP, "THUMB_IP", "carpal_interphalangeal_1"],
[mp_hands.THUMB_TIP, "THUMB_TIP", "carpal_distal_phalanx_1"],
[mp_hands.INDEX_FINGER_MCP, "INDEX_FINGER_MCP", "metacarpophalangeal_2"],
[mp_hands.INDEX_FINGER_PIP, "INDEX_FINGER_PIP", "carpal_proximal_interphalangeal_2"],
[mp_hands.INDEX_FINGER_DIP, "INDEX_FINGER_DIP", "carpal_distal_interphalangeal_2"],
[mp_hands.INDEX_FINGER_TIP, "INDEX_FINGER_TIP", "carpal_distal_phalanx_2"],
[mp_hands.MIDDLE_FINGER_MCP, "MIDDLE_FINGER_MCP", "metacarpophalangeal_3"],
[mp_hands.MIDDLE_FINGER_PIP, "MIDDLE_FINGER_PIP", "carpal_proximal_interphalangeal_3"],
[mp_hands.MIDDLE_FINGER_DIP, "MIDDLE_FINGER_DIP", "carpal_distal_interphalangeal_3"],
[mp_hands.MIDDLE_FINGER_TIP, "MIDDLE_FINGER_TIP", "carpal_distal_phalanx_3"],
[mp_hands.RING_FINGER_MCP, "RING_FINGER_MCP", "metacarpophalangeal_4"],
[mp_hands.RING_FINGER_PIP, "RING_FINGER_PIP", "carpal_proximal_interphalangeal_4"],
[mp_hands.RING_FINGER_DIP, "RING_FINGER_DIP", "carpal_distal_interphalangeal_4"],
[mp_hands.RING_FINGER_TIP, "RING_FINGER_TIP", "carpal_distal_phalanx_4"],
[mp_hands.PINKY_MCP, "PINKY_MCP", "metacarpophalangeal_5"],
[mp_hands.PINKY_PIP, "PINKY_PIP", "carpal_proximal_interphalangeal_5"],
[mp_hands.PINKY_DIP, "PINKY_DIP", "carpal_distal_interphalangeal_5"],
[mp_hands.PINKY_TIP, "PINKY_TIP", "carpal_distal_phalanx_5"]]

pose = [
[poselm.NOSE, 0, "nose"],
[poselm.LEFT_EYE_INNER, 1, "l_eye_inner"],
[poselm.LEFT_EYE, 2, "l_eye"],
[poselm.LEFT_EYE_OUTER, 3, "l_eye_outer"],
[poselm.RIGHT_EYE_INNER, 4, "r_eye_inner"],
[poselm.RIGHT_EYE, 5, "r_eye"],
[poselm.RIGHT_EYE_OUTER, 6, "r_eye_outer"],
[poselm.LEFT_EAR, 7, "l_ear"],
[poselm.RIGHT_EAR, 8, "r_ear"],
[poselm.MOUTH_LEFT, 9, "l_mouth"],
[poselm.MOUTH_RIGHT, 10, "r_mouth"],
[poselm.LEFT_SHOULDER, 11, "l_shoulder"],
[poselm.RIGHT_SHOULDER, 12, "r_shoulder"],
[poselm.LEFT_ELBOW, 13, "l_elbow"],
[poselm.RIGHT_ELBOW, 14, "r_elbow"],
[poselm.LEFT_WRIST, 15, "l_wrist"],
[poselm.RIGHT_WRIST, 16, "r_wrist"],
[poselm.LEFT_PINKY, 17, "l_pinky"],
[poselm.RIGHT_PINKY, 18, "r_pinky"],
[poselm.LEFT_INDEX, 19, "l_index"],
[poselm.RIGHT_INDEX, 20, "r_index"],
[poselm.LEFT_THUMB, 21, "l_thumb"],
[poselm.RIGHT_THUMB, 22, "r_thumb"],
[poselm.LEFT_HIP, 23, "l_hip"],
[poselm.RIGHT_HIP, 24, "r_hip"],
[poselm.LEFT_KNEE, 25, "l_knee"],
[poselm.RIGHT_KNEE, 26, "r_knee"],
[poselm.LEFT_ANKLE, 27, "l_ankle"],
[poselm.RIGHT_ANKLE, 28, "r_ankle"],
[poselm.LEFT_HEEL, 29, "l_heel"],
[poselm.RIGHT_HEEL, 30, "r_heel"],
[poselm.LEFT_FOOT_INDEX, 31, "l_foot_index"],
[poselm.RIGHT_FOOT_INDEX, 32, "r_foot_index"]
]

face = [
[ 0 ,  0 ,  "0"],
[ 1 ,  1 ,  "1"],
[ 2 ,  2 ,  "2"],
[ 3 ,  3 ,  "3"],
[ 4 ,  4 ,  "4"],
[ 5 ,  5 ,  "5"],
[ 6 ,  6 ,  "6"],
[ 7 ,  7 ,  "7"],
[ 8 ,  8 ,  "8"],
[ 9 ,  9 ,  "9"],
[ 10 ,  10 ,  "10"],
[ 11 ,  11 ,  "11"],
[ 12 ,  12 ,  "12"],
[ 13 ,  13 ,  "13"],
[ 14 ,  14 ,  "14"],
[ 15 ,  15 ,  "15"],
[ 16 ,  16 ,  "16"],
[ 17 ,  17 ,  "17"],
[ 18 ,  18 ,  "18"],
[ 19 ,  19 ,  "19"],
[ 20 ,  20 ,  "20"],
[ 21 ,  21 ,  "21"],
[ 22 ,  22 ,  "22"],
[ 23 ,  23 ,  "23"],
[ 24 ,  24 ,  "24"],
[ 25 ,  25 ,  "25"],
[ 26 ,  26 ,  "26"],
[ 27 ,  27 ,  "27"],
[ 28 ,  28 ,  "28"],
[ 29 ,  29 ,  "29"],
[ 30 ,  30 ,  "30"],
[ 31 ,  31 ,  "31"],
[ 32 ,  32 ,  "32"],
[ 33 ,  33 ,  "33"],
[ 34 ,  34 ,  "34"],
[ 35 ,  35 ,  "35"],
[ 36 ,  36 ,  "36"],
[ 37 ,  37 ,  "37"],
[ 38 ,  38 ,  "38"],
[ 39 ,  39 ,  "39"],
[ 40 ,  40 ,  "40"],
[ 41 ,  41 ,  "41"],
[ 42 ,  42 ,  "42"],
[ 43 ,  43 ,  "43"],
[ 44 ,  44 ,  "44"],
[ 45 ,  45 ,  "45"],
[ 46 ,  46 ,  "46"],
[ 47 ,  47 ,  "47"],
[ 48 ,  48 ,  "48"],
[ 49 ,  49 ,  "49"],
[ 50 ,  50 ,  "50"],
[ 51 ,  51 ,  "51"],
[ 52 ,  52 ,  "52"],
[ 53 ,  53 ,  "53"],
[ 54 ,  54 ,  "54"],
[ 55 ,  55 ,  "55"],
[ 56 ,  56 ,  "56"],
[ 57 ,  57 ,  "57"],
[ 58 ,  58 ,  "58"],
[ 59 ,  59 ,  "59"],
[ 60 ,  60 ,  "60"],
[ 61 ,  61 ,  "61"],
[ 62 ,  62 ,  "62"],
[ 63 ,  63 ,  "63"],
[ 64 ,  64 ,  "64"],
[ 65 ,  65 ,  "65"],
[ 66 ,  66 ,  "66"],
[ 67 ,  67 ,  "67"],
[ 68 ,  68 ,  "68"],
[ 69 ,  69 ,  "69"],
[ 70 ,  70 ,  "70"],
[ 71 ,  71 ,  "71"],
[ 72 ,  72 ,  "72"],
[ 73 ,  73 ,  "73"],
[ 74 ,  74 ,  "74"],
[ 75 ,  75 ,  "75"],
[ 76 ,  76 ,  "76"],
[ 77 ,  77 ,  "77"],
[ 78 ,  78 ,  "78"],
[ 79 ,  79 ,  "79"],
[ 80 ,  80 ,  "80"],
[ 81 ,  81 ,  "81"],
[ 82 ,  82 ,  "82"],
[ 83 ,  83 ,  "83"],
[ 84 ,  84 ,  "84"],
[ 85 ,  85 ,  "85"],
[ 86 ,  86 ,  "86"],
[ 87 ,  87 ,  "87"],
[ 88 ,  88 ,  "88"],
[ 89 ,  89 ,  "89"],
[ 90 ,  90 ,  "90"],
[ 91 ,  91 ,  "91"],
[ 92 ,  92 ,  "92"],
[ 93 ,  93 ,  "93"],
[ 94 ,  94 ,  "94"],
[ 95 ,  95 ,  "95"],
[ 96 ,  96 ,  "96"],
[ 97 ,  97 ,  "97"],
[ 98 ,  98 ,  "98"],
[ 99 ,  99 ,  "99"],
[ 100 ,  100 ,  "100"],
[ 101 ,  101 ,  "101"],
[ 102 ,  102 ,  "102"],
[ 103 ,  103 ,  "103"],
[ 104 ,  104 ,  "104"],
[ 105 ,  105 ,  "105"],
[ 106 ,  106 ,  "106"],
[ 107 ,  107 ,  "107"],
[ 108 ,  108 ,  "108"],
[ 109 ,  109 ,  "109"],
[ 110 ,  110 ,  "110"],
[ 111 ,  111 ,  "111"],
[ 112 ,  112 ,  "112"],
[ 113 ,  113 ,  "113"],
[ 114 ,  114 ,  "114"],
[ 115 ,  115 ,  "115"],
[ 116 ,  116 ,  "116"],
[ 117 ,  117 ,  "117"],
[ 118 ,  118 ,  "118"],
[ 119 ,  119 ,  "119"],
[ 120 ,  120 ,  "120"],
[ 121 ,  121 ,  "121"],
[ 122 ,  122 ,  "122"],
[ 123 ,  123 ,  "123"],
[ 124 ,  124 ,  "124"],
[ 125 ,  125 ,  "125"],
[ 126 ,  126 ,  "126"],
[ 127 ,  127 ,  "127"],
[ 128 ,  128 ,  "128"],
[ 129 ,  129 ,  "129"],
[ 130 ,  130 ,  "130"],
[ 131 ,  131 ,  "131"],
[ 132 ,  132 ,  "132"],
[ 133 ,  133 ,  "133"],
[ 134 ,  134 ,  "134"],
[ 135 ,  135 ,  "135"],
[ 136 ,  136 ,  "136"],
[ 137 ,  137 ,  "137"],
[ 138 ,  138 ,  "138"],
[ 139 ,  139 ,  "139"],
[ 140 ,  140 ,  "140"],
[ 141 ,  141 ,  "141"],
[ 142 ,  142 ,  "142"],
[ 143 ,  143 ,  "143"],
[ 144 ,  144 ,  "144"],
[ 145 ,  145 ,  "145"],
[ 146 ,  146 ,  "146"],
[ 147 ,  147 ,  "147"],
[ 148 ,  148 ,  "148"],
[ 149 ,  149 ,  "149"],
[ 150 ,  150 ,  "150"],
[ 151 ,  151 ,  "151"],
[ 152 ,  152 ,  "152"],
[ 153 ,  153 ,  "153"],
[ 154 ,  154 ,  "154"],
[ 155 ,  155 ,  "155"],
[ 156 ,  156 ,  "156"],
[ 157 ,  157 ,  "157"],
[ 158 ,  158 ,  "158"],
[ 159 ,  159 ,  "159"],
[ 160 ,  160 ,  "160"],
[ 161 ,  161 ,  "161"],
[ 162 ,  162 ,  "162"],
[ 163 ,  163 ,  "163"],
[ 164 ,  164 ,  "164"],
[ 165 ,  165 ,  "165"],
[ 166 ,  166 ,  "166"],
[ 167 ,  167 ,  "167"],
[ 168 ,  168 ,  "168"],
[ 169 ,  169 ,  "169"],
[ 170 ,  170 ,  "170"],
[ 171 ,  171 ,  "171"],
[ 172 ,  172 ,  "172"],
[ 173 ,  173 ,  "173"],
[ 174 ,  174 ,  "174"],
[ 175 ,  175 ,  "175"],
[ 176 ,  176 ,  "176"],
[ 177 ,  177 ,  "177"],
[ 178 ,  178 ,  "178"],
[ 179 ,  179 ,  "179"],
[ 180 ,  180 ,  "180"],
[ 181 ,  181 ,  "181"],
[ 182 ,  182 ,  "182"],
[ 183 ,  183 ,  "183"],
[ 184 ,  184 ,  "184"],
[ 185 ,  185 ,  "185"],
[ 186 ,  186 ,  "186"],
[ 187 ,  187 ,  "187"],
[ 188 ,  188 ,  "188"],
[ 189 ,  189 ,  "189"],
[ 190 ,  190 ,  "190"],
[ 191 ,  191 ,  "191"],
[ 192 ,  192 ,  "192"],
[ 193 ,  193 ,  "193"],
[ 194 ,  194 ,  "194"],
[ 195 ,  195 ,  "195"],
[ 196 ,  196 ,  "196"],
[ 197 ,  197 ,  "197"],
[ 198 ,  198 ,  "198"],
[ 199 ,  199 ,  "199"],
[ 200 ,  200 ,  "200"],
[ 201 ,  201 ,  "201"],
[ 202 ,  202 ,  "202"],
[ 203 ,  203 ,  "203"],
[ 204 ,  204 ,  "204"],
[ 205 ,  205 ,  "205"],
[ 206 ,  206 ,  "206"],
[ 207 ,  207 ,  "207"],
[ 208 ,  208 ,  "208"],
[ 209 ,  209 ,  "209"],
[ 210 ,  210 ,  "210"],
[ 211 ,  211 ,  "211"],
[ 212 ,  212 ,  "212"],
[ 213 ,  213 ,  "213"],
[ 214 ,  214 ,  "214"],
[ 215 ,  215 ,  "215"],
[ 216 ,  216 ,  "216"],
[ 217 ,  217 ,  "217"],
[ 218 ,  218 ,  "218"],
[ 219 ,  219 ,  "219"],
[ 220 ,  220 ,  "220"],
[ 221 ,  221 ,  "221"],
[ 222 ,  222 ,  "222"],
[ 223 ,  223 ,  "223"],
[ 224 ,  224 ,  "224"],
[ 225 ,  225 ,  "225"],
[ 226 ,  226 ,  "226"],
[ 227 ,  227 ,  "227"],
[ 228 ,  228 ,  "228"],
[ 229 ,  229 ,  "229"],
[ 230 ,  230 ,  "230"],
[ 231 ,  231 ,  "231"],
[ 232 ,  232 ,  "232"],
[ 233 ,  233 ,  "233"],
[ 234 ,  234 ,  "234"],
[ 235 ,  235 ,  "235"],
[ 236 ,  236 ,  "236"],
[ 237 ,  237 ,  "237"],
[ 238 ,  238 ,  "238"],
[ 239 ,  239 ,  "239"],
[ 240 ,  240 ,  "240"],
[ 241 ,  241 ,  "241"],
[ 242 ,  242 ,  "242"],
[ 243 ,  243 ,  "243"],
[ 244 ,  244 ,  "244"],
[ 245 ,  245 ,  "245"],
[ 246 ,  246 ,  "246"],
[ 247 ,  247 ,  "247"],
[ 248 ,  248 ,  "248"],
[ 249 ,  249 ,  "249"],
[ 250 ,  250 ,  "250"],
[ 251 ,  251 ,  "251"],
[ 252 ,  252 ,  "252"],
[ 253 ,  253 ,  "253"],
[ 254 ,  254 ,  "254"],
[ 255 ,  255 ,  "255"],
[ 256 ,  256 ,  "256"],
[ 257 ,  257 ,  "257"],
[ 258 ,  258 ,  "258"],
[ 259 ,  259 ,  "259"],
[ 260 ,  260 ,  "260"],
[ 261 ,  261 ,  "261"],
[ 262 ,  262 ,  "262"],
[ 263 ,  263 ,  "263"],
[ 264 ,  264 ,  "264"],
[ 265 ,  265 ,  "265"],
[ 266 ,  266 ,  "266"],
[ 267 ,  267 ,  "267"],
[ 268 ,  268 ,  "268"],
[ 269 ,  269 ,  "269"],
[ 270 ,  270 ,  "270"],
[ 271 ,  271 ,  "271"],
[ 272 ,  272 ,  "272"],
[ 273 ,  273 ,  "273"],
[ 274 ,  274 ,  "274"],
[ 275 ,  275 ,  "275"],
[ 276 ,  276 ,  "276"],
[ 277 ,  277 ,  "277"],
[ 278 ,  278 ,  "278"],
[ 279 ,  279 ,  "279"],
[ 280 ,  280 ,  "280"],
[ 281 ,  281 ,  "281"],
[ 282 ,  282 ,  "282"],
[ 283 ,  283 ,  "283"],
[ 284 ,  284 ,  "284"],
[ 285 ,  285 ,  "285"],
[ 286 ,  286 ,  "286"],
[ 287 ,  287 ,  "287"],
[ 288 ,  288 ,  "288"],
[ 289 ,  289 ,  "289"],
[ 290 ,  290 ,  "290"],
[ 291 ,  291 ,  "291"],
[ 292 ,  292 ,  "292"],
[ 293 ,  293 ,  "293"],
[ 294 ,  294 ,  "294"],
[ 295 ,  295 ,  "295"],
[ 296 ,  296 ,  "296"],
[ 297 ,  297 ,  "297"],
[ 298 ,  298 ,  "298"],
[ 299 ,  299 ,  "299"],
[ 300 ,  300 ,  "300"],
[ 301 ,  301 ,  "301"],
[ 302 ,  302 ,  "302"],
[ 303 ,  303 ,  "303"],
[ 304 ,  304 ,  "304"],
[ 305 ,  305 ,  "305"],
[ 306 ,  306 ,  "306"],
[ 307 ,  307 ,  "307"],
[ 308 ,  308 ,  "308"],
[ 309 ,  309 ,  "309"],
[ 310 ,  310 ,  "310"],
[ 311 ,  311 ,  "311"],
[ 312 ,  312 ,  "312"],
[ 313 ,  313 ,  "313"],
[ 314 ,  314 ,  "314"],
[ 315 ,  315 ,  "315"],
[ 316 ,  316 ,  "316"],
[ 317 ,  317 ,  "317"],
[ 318 ,  318 ,  "318"],
[ 319 ,  319 ,  "319"],
[ 320 ,  320 ,  "320"],
[ 321 ,  321 ,  "321"],
[ 322 ,  322 ,  "322"],
[ 323 ,  323 ,  "323"],
[ 324 ,  324 ,  "324"],
[ 325 ,  325 ,  "325"],
[ 326 ,  326 ,  "326"],
[ 327 ,  327 ,  "327"],
[ 328 ,  328 ,  "328"],
[ 329 ,  329 ,  "329"],
[ 330 ,  330 ,  "330"],
[ 331 ,  331 ,  "331"],
[ 332 ,  332 ,  "332"],
[ 333 ,  333 ,  "333"],
[ 334 ,  334 ,  "334"],
[ 335 ,  335 ,  "335"],
[ 336 ,  336 ,  "336"],
[ 337 ,  337 ,  "337"],
[ 338 ,  338 ,  "338"],
[ 339 ,  339 ,  "339"],
[ 340 ,  340 ,  "340"],
[ 341 ,  341 ,  "341"],
[ 342 ,  342 ,  "342"],
[ 343 ,  343 ,  "343"],
[ 344 ,  344 ,  "344"],
[ 345 ,  345 ,  "345"],
[ 346 ,  346 ,  "346"],
[ 347 ,  347 ,  "347"],
[ 348 ,  348 ,  "348"],
[ 349 ,  349 ,  "349"],
[ 350 ,  350 ,  "350"],
[ 351 ,  351 ,  "351"],
[ 352 ,  352 ,  "352"],
[ 353 ,  353 ,  "353"],
[ 354 ,  354 ,  "354"],
[ 355 ,  355 ,  "355"],
[ 356 ,  356 ,  "356"],
[ 357 ,  357 ,  "357"],
[ 358 ,  358 ,  "358"],
[ 359 ,  359 ,  "359"],
[ 360 ,  360 ,  "360"],
[ 361 ,  361 ,  "361"],
[ 362 ,  362 ,  "362"],
[ 363 ,  363 ,  "363"],
[ 364 ,  364 ,  "364"],
[ 365 ,  365 ,  "365"],
[ 366 ,  366 ,  "366"],
[ 367 ,  367 ,  "367"],
[ 368 ,  368 ,  "368"],
[ 369 ,  369 ,  "369"],
[ 370 ,  370 ,  "370"],
[ 371 ,  371 ,  "371"],
[ 372 ,  372 ,  "372"],
[ 373 ,  373 ,  "373"],
[ 374 ,  374 ,  "374"],
[ 375 ,  375 ,  "375"],
[ 376 ,  376 ,  "376"],
[ 377 ,  377 ,  "377"],
[ 378 ,  378 ,  "378"],
[ 379 ,  379 ,  "379"],
[ 380 ,  380 ,  "380"],
[ 381 ,  381 ,  "381"],
[ 382 ,  382 ,  "382"],
[ 383 ,  383 ,  "383"],
[ 384 ,  384 ,  "384"],
[ 385 ,  385 ,  "385"],
[ 386 ,  386 ,  "386"],
[ 387 ,  387 ,  "387"],
[ 388 ,  388 ,  "388"],
[ 389 ,  389 ,  "389"],
[ 390 ,  390 ,  "390"],
[ 391 ,  391 ,  "391"],
[ 392 ,  392 ,  "392"],
[ 393 ,  393 ,  "393"],
[ 394 ,  394 ,  "394"],
[ 395 ,  395 ,  "395"],
[ 396 ,  396 ,  "396"],
[ 397 ,  397 ,  "397"],
[ 398 ,  398 ,  "398"],
[ 399 ,  399 ,  "399"],
[ 400 ,  400 ,  "400"],
[ 401 ,  401 ,  "401"],
[ 402 ,  402 ,  "402"],
[ 403 ,  403 ,  "403"],
[ 404 ,  404 ,  "404"],
[ 405 ,  405 ,  "405"],
[ 406 ,  406 ,  "406"],
[ 407 ,  407 ,  "407"],
[ 408 ,  408 ,  "408"],
[ 409 ,  409 ,  "409"],
[ 410 ,  410 ,  "410"],
[ 411 ,  411 ,  "411"],
[ 412 ,  412 ,  "412"],
[ 413 ,  413 ,  "413"],
[ 414 ,  414 ,  "414"],
[ 415 ,  415 ,  "415"],
[ 416 ,  416 ,  "416"],
[ 417 ,  417 ,  "417"],
[ 418 ,  418 ,  "418"],
[ 419 ,  419 ,  "419"],
[ 420 ,  420 ,  "420"],
[ 421 ,  421 ,  "421"],
[ 422 ,  422 ,  "422"],
[ 423 ,  423 ,  "423"],
[ 424 ,  424 ,  "424"],
[ 425 ,  425 ,  "425"],
[ 426 ,  426 ,  "426"],
[ 427 ,  427 ,  "427"],
[ 428 ,  428 ,  "428"],
[ 429 ,  429 ,  "429"],
[ 430 ,  430 ,  "430"],
[ 431 ,  431 ,  "431"],
[ 432 ,  432 ,  "432"],
[ 433 ,  433 ,  "433"],
[ 434 ,  434 ,  "434"],
[ 435 ,  435 ,  "435"],
[ 436 ,  436 ,  "436"],
[ 437 ,  437 ,  "437"],
[ 438 ,  438 ,  "438"],
[ 439 ,  439 ,  "439"],
[ 440 ,  440 ,  "440"],
[ 441 ,  441 ,  "441"],
[ 442 ,  442 ,  "442"],
[ 443 ,  443 ,  "443"],
[ 444 ,  444 ,  "444"],
[ 445 ,  445 ,  "445"],
[ 446 ,  446 ,  "446"],
[ 447 ,  447 ,  "447"],
[ 448 ,  448 ,  "448"],
[ 449 ,  449 ,  "449"],
[ 450 ,  450 ,  "450"],
[ 451 ,  451 ,  "451"],
[ 452 ,  452 ,  "452"],
[ 453 ,  453 ,  "453"],
[ 454 ,  454 ,  "454"],
[ 455 ,  455 ,  "455"],
[ 456 ,  456 ,  "456"],
[ 457 ,  457 ,  "457"],
[ 458 ,  458 ,  "458"],
[ 459 ,  459 ,  "459"],
[ 460 ,  460 ,  "460"],
[ 461 ,  461 ,  "461"],
[ 462 ,  462 ,  "462"],
[ 463 ,  463 ,  "463"],
[ 464 ,  464 ,  "464"],
[ 465 ,  465 ,  "465"],
[ 466 ,  466 ,  "466"],
[ 467 ,  467 ,  "467"]
]

# Load the MediaPipe Sign Language Detection model
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Load the MediaPipe Drawing utils for visualization
mp_drawing = mp.solutions.drawing_utils

# load MedidPipe hands solutions

# Load the video file
# video_path = "path_to_video_file.mp4"
video_path = 0
cap = cv2.VideoCapture(video_path)



MyLandmark = namedtuple('MyLandmark', 'x y z visibility')
# sendMessages()
class myClient():
    def __init__(self):
        self.buffer = []
        self.nick =    [ sys.argv[1] ]

        print(f"Using socket.io custom protocol, see sendMessage")

        self.sequenceno = -1
        self.connection_counter = 0


    def startedEvent(self):
        print('started event')

    def performAnAction(self):
        # print('performed an action')
        if cap.isOpened():
            retval, frame = cap.read()
            if retval:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect the signs in the frame
                results = holistic.process(image)

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                #signs = []
                #if results.pose_landmarks:
                #    sign = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW].visibility
                #    signs.append(sign)

                # Comment out these lines as desired.  Please don't delete them
                self.sendAll(image, results.left_hand_landmarks, "l", mp_holistic.HAND_CONNECTIONS, hand)
                self.sendAll(image, results.right_hand_landmarks, "r", mp_holistic.HAND_CONNECTIONS, hand)
                self.sendAll(image, results.pose_landmarks, "p", mp_holistic.POSE_CONNECTIONS, pose)
                # These are a big performance hit
                #self.sendAll(image, results.face_landmarks, "t", mp_holistic.FACEMESH_TESSELATION, face)
                #self.sendAll(image, results.face_landmarks, "c", mp_holistic.FACEMESH_CONTOURS, face)

                # Display the frame
                cv2.imshow("Sign Language Detection", image)
                # Break the loop if ESC is pressed
                if cv2.waitKey(30) == 27:
                    self.bufferSend()
                    print("Stopping")
                    return False
        else:
            print("Video died")
        self.bufferSend()
        return True

    def sendAll(self, image, landmarks, suffix, connections, lmlist):
        # send lines to refresh the screen
        self.sendLines(connections, suffix)   # left hand
        # construct each time, because they disappear
        # self.constructPoints(landmarks, "_"+suffix, lmlist)
        # send coordinates
        self.sendPoints(image, landmarks, "_"+suffix, connections, lmlist)

    def constructPoints(self, landmarks, suffix, lmlist):
        if landmarks:
            for landmark in lmlist:
                self.constructPoint(landmark[0], suffix, landmark[2])
            if suffix in ("_p"):
                self.constructPoint(len(lmlist), suffix, "sacroiliac")
                self.constructPoint(len(lmlist)+1, suffix, "vc7")

    def sendPoints(self, image, landmarks, suffix, connections, lmlist):
        mp_drawing.draw_landmarks(image, landmarks, connections)
        if landmarks:
            if suffix in ("_p"):
                for landmark in lmlist:
                    lmk = landmarks.landmark[landmark[0]]
                    # get rid of entire hands in pose landmarks
                    if landmark[0] < poselm.LEFT_WRIST or landmark[0] > poselm.RIGHT_THUMB:
                        self.constructPoint(landmark[0], suffix, landmark[2])
                        self.sendPoint(lmk, landmark[0], suffix, landmark[2], image)
                # add extra joints
                self.constructPoint(len(lmlist), suffix, "sacroiliac")

                # average left and right hip
                lhlmk = landmarks.landmark[poselm.LEFT_HIP] 
                rhlmk = landmarks.landmark[poselm.RIGHT_HIP] 
                lmk = MyLandmark(
                       x= (lhlmk.x + rhlmk.x)/2,
                       y= (lhlmk.y + rhlmk.y)/2,
                       z= (lhlmk.z + rhlmk.z)/2,
                       visibility=(lhlmk.visibility + rhlmk.visibility)/2  )
                self.sendPoint(lmk, len(lmlist), suffix, "sacroiliac", image)

                # average left and right shoulder
                self.constructPoint(len(lmlist)+1, suffix, "vc7")
                lslmk = landmarks.landmark[poselm.LEFT_SHOULDER] 
                rslmk = landmarks.landmark[poselm.RIGHT_SHOULDER] 
                lmk = MyLandmark(
                       x= (lslmk.x + rslmk.x)/2,
                       y= (lslmk.y + rslmk.y)/2,
                       z= (lslmk.z + rslmk.z)/2,
                       visibility=(lslmk.visibility + rslmk.visibility)/2  )
                self.sendPoint(lmk, len(lmlist)+1, suffix, "vc7", image)

            elif suffix in ("_l", "_r", "_t", "_c"):
                for landmark in lmlist:
                    lmk = landmarks.landmark[landmark[0]]
                    self.constructPoint(landmark[0], suffix, landmark[2])
                    self.sendPoint(lmk, landmark[0], suffix, landmark[2], image)

    def sendMPLine(self, fr, to):
        variable = f"{self.connection_counter}"
        for i in range(len(self.nick)):
            self.bufferMessage(f'{self.nick[i]}|S|{variable}|U|{fr}|{to}')
        self.connection_counter = self.connection_counter + 1

        if self.connection_counter < 0:  # wrap around, I hope
            self.connection_counter = 0

    def sendLines(self, connections, prefix):
        for connection in connections:
            # make sure not to draw these lines
            if prefix == "p" and connection[0] == poselm.LEFT_SHOULDER and connection[1] == poselm.LEFT_HIP:
                pass
            elif prefix == "p" and connection[0] == poselm.LEFT_SHOULDER and connection[1] == poselm.RIGHT_SHOULDER:
                pass
            elif prefix == "p" and connection[0] == poselm.RIGHT_SHOULDER and connection[1] == poselm.RIGHT_HIP:
                pass
            else:
                self.sendMPLine(f"{prefix}{connection[0]}", f"{prefix}{connection[1]}")
        # draw these lines instead
        if prefix in ("p"):
            self.sendMPLine(f"p34", f"p11") # patch the vc7 to the left shoulder
            self.sendMPLine(f"p34", f"p12") # patch the vc7 to the right shoulder
            self.sendMPLine(f"p33", f"p34") # patch the sacroiliac to vc7
            self.sendMPLine(f"p13", f"l0")  # patch the left elbow to the left wrist
            self.sendMPLine(f"p14", f"r0")  # patch the right elbow to the right wrist

    def connectionMade(self):
        self.sendMessage("Marker: Start")  # Send marker for the first frame
        self.buffer = []
        self.runRecognizer()


    def sendMessage(self, message):
        entiremessage = ""

        timestamp = time.time()
        entiremessage += str(int(timestamp))
        entiremessage += "|"

        self.sequenceno += 1
        entiremessage += str(self.sequenceno)
        entiremessage += ","

        entiremessage += message
        # print(entiremessage)
        sio.emit('python_clientavatar', entiremessage.encode())

    def bufferSend(self):
        message = " ".join(self.buffer)+"\n"
        # print(message)
        self.sendMessage(message)
        self.buffer = []

    def bufferMessage(self, message):
        # print(f"{message}\n");
        self.buffer.append(message);

    def constructMPPoint(self, landmark, suffix, joint_string):
        prefix = suffix[1:]
        ptid = f"{prefix}{landmark}"
        for i in range(len(self.nick)):
            self.bufferMessage(f'{self.nick[i]}|J|{ptid}|I|0.0|0.0|0.0|{joint_string}')

    def constructPoint(self, landmark, suffix, joint_string: str):
        prefix = suffix[1:]+"_"
        if prefix == "p_" and (joint_string.startswith("l_") or joint_string.startswith("r_")):
            prefix = ""
        self.constructMPPoint(landmark, suffix, joint_string)

    def sendMPPoint(self, landmark, suffix, x, y, z, joint_string):
        prefix = suffix[1:]
        ptid = f"{prefix}{landmark}"
        for i in range(len(self.nick)):
            self.bufferMessage(f'{self.nick[i]}|J|{ptid}|U|{x}|{y}|{z}|{joint_string}')

    def sendPoint(self, lmk, landmark, suffix, joint_string: str, image):

        # print(lmk)
        
        x = round(lmk.x, 5)
        y = round(lmk.y, 5)
        z = round(lmk.z, 5)
        v = lmk.visibility
        shape = image.shape

        self.sendMPPoint(landmark, suffix, x, y, z, joint_string)
        # print(v)
        relative_x = int(x * shape[1])
        relative_y = int(y * shape[0])
        #relative_z = int(z * shape[2])
        #self.bufferMessage(f"XR:{relative_x}")
        #self.bufferMessage(f"YR:{relative_y}")
        #self.bufferMessage(f"ZR:{relative_z}")
        prefix = suffix[1:]+"_"
        if prefix == "p_" and joint_string.startswith("l_"):
            prefix = ""
        elif prefix == "p_" and joint_string.startswith("r_"):
            prefix = ""
        # cv2.putText(img=image, text=prefix+joint_string, org=(relative_x, relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img=image, text=f"{x} {y} {z}", org=(relative_x, relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)

    def runRecognizer(self):
        certainAmount = 5.0  # this is in seconds


def main():
    try:
        client = myClient()
        # Connect to the Socket.IO server
        # Replace with your server's URL
        server_url = 'http://localhost:8088'
        print(f"Connecting to {server_url}...")
        sio.connect(server_url)
        
        # Send a message to the server
        sio.emit('clientjoin', "VideoFeed")  # TODO somethimg better than this
        sio.emit('clientactivesession', "yottzumm")
        sio.emit('clientactivename', "VideoFeed")
        
        # Keep the client running to receive events
        try:
            while client.performAnAction():
                # Send a periodic message every 5 seconds
                sio.emit('ping', {'timestamp': time.time()})
                time.sleep(0)
                
        except KeyboardInterrupt:
            print("Client stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Disconnect from the server
        if sio.connected:
            sio.disconnect()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
