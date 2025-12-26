<?php
/**
 * Standalone PHP OSC Server
 * Receives and parses OSC messages over UDP
 * No external dependencies required
 */

class OSCServer {
    private $socket;
    private $address;
    private $port;
    
    public function __construct($address = '0.0.0.0', $port = 8000) {
        $this->address = $address;
        $this->port = $port;
        
        // Create UDP socket
        $this->socket = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
        if (!$this->socket) {
            throw new Exception("Could not create socket: " . socket_strerror(socket_last_error()));
        }
        
        // Set socket options
        socket_set_option($this->socket, SOL_SOCKET, SO_REUSEADDR, 1);
        
        // Bind to address and port
        if (!socket_bind($this->socket, $this->address, $this->port)) {
            throw new Exception("Could not bind to $address:$port: " . socket_strerror(socket_last_error($this->socket)));
        }
        
        echo "OSC Server listening on $address:$port\n";
        echo "Press Ctrl+C to stop\n\n";
    }
    
    /**
     * Start listening for OSC messages
     * @param callable|null $callback Custom message handler
     */
    public function listen($callback = null) {
        $from = '';
        $port = 0;
        $buffer = '';
        
        while (true) {
            // Receive data from socket (blocking)
            $bytes = socket_recvfrom($this->socket, $buffer, 65536, 0, $from, $port);
            
            if ($bytes === false) {
                $error = socket_last_error($this->socket);
                echo "Socket error: " . socket_strerror($error) . "\n";
                continue;
            }
            
            if ($bytes > 0) {
                try {
                    $message = $this->parseOSCMessage($buffer);
                    
                    if ($callback && is_callable($callback)) {
                        $callback($message, $from, $port);
                    } else {
                        $this->defaultHandler($message, $from, $port);
                    }
                } catch (Exception $e) {
                    echo "Error parsing OSC message: " . $e->getMessage() . "\n";
                }
            }
        }
    }
    
    /**
     * Parse OSC message from binary data
     * @param string $data Binary OSC message data
     * @return array Parsed message with address, typetags, and arguments
     */
    private function parseOSCMessage($data) {
        $result = [
            'address' => '',
            'typetags' => '',
            'arguments' => []
        ];
        
        $pos = 0;
        $len = strlen($data);
        
        // Parse OSC address (null-terminated string)
        $nullPos = strpos($data, "\0", $pos);
        if ($nullPos === false) {
            throw new Exception("Invalid OSC message: no address found");
        }
        
        $result['address'] = substr($data, $pos, $nullPos - $pos);
        $pos = $this->alignTo4($nullPos + 1);
        
        // Check if we have type tags
        if ($pos >= $len) {
            return $result; // Message with only address, no arguments
        }
        
        // Parse type tags (starts with comma)
        if ($data[$pos] !== ',') {
            // No type tags - old-style OSC message
            return $result;
        }
        
        $nullPos = strpos($data, "\0", $pos);
        if ($nullPos === false) {
            throw new Exception("Invalid OSC message: malformed type tags");
        }
        
        $result['typetags'] = substr($data, $pos, $nullPos - $pos);
        $pos = $this->alignTo4($nullPos + 1);
        
        // Parse arguments based on type tags
        $typeTagCount = strlen($result['typetags']);
        for ($i = 1; $i < $typeTagCount; $i++) {
            if ($pos >= $len) {
                break; // No more data
            }
            
            $type = $result['typetags'][$i];
            
            switch ($type) {
                case 'i': // int32
                    if ($pos + 4 > $len) {
                        throw new Exception("Unexpected end of data reading int32");
                    }
                    $value = unpack('N', substr($data, $pos, 4))[1];
                    // Convert from unsigned to signed
                    if ($value > 0x7FFFFFFF) {
                        $value = $value - 0x100000000;
                    }
                    $result['arguments'][] = $value;
                    $pos += 4;
                    break;
                    
                case 'f': // float32
                    if ($pos + 4 > $len) {
                        throw new Exception("Unexpected end of data reading float32");
                    }
                    $packed = substr($data, $pos, 4);
                    $unpacked = unpack('N', $packed)[1];
                    $result['arguments'][] = unpack('f', pack('L', $unpacked))[1];
                    $pos += 4;
                    break;
                    
                case 's': // string
                    $nullPos = strpos($data, "\0", $pos);
                    if ($nullPos === false) {
                        throw new Exception("Unexpected end of data reading string");
                    }
                    $result['arguments'][] = substr($data, $pos, $nullPos - $pos);
                    $pos = $this->alignTo4($nullPos + 1);
                    break;
                    
                case 'b': // blob
                    if ($pos + 4 > $len) {
                        throw new Exception("Unexpected end of data reading blob size");
                    }
                    $size = unpack('N', substr($data, $pos, 4))[1];
                    $pos += 4;
                    if ($pos + $size > $len) {
                        throw new Exception("Unexpected end of data reading blob");
                    }
                    $result['arguments'][] = substr($data, $pos, $size);
                    $pos = $this->alignTo4($pos + $size);
                    break;
                    
                case 'T': // True
                    $result['arguments'][] = true;
                    break;
                    
                case 'F': // False
                    $result['arguments'][] = false;
                    break;
                    
                case 'N': // Null/Nil
                    $result['arguments'][] = null;
                    break;
                    
                case 'I': // Impulse (Infinitum)
                    $result['arguments'][] = INF;
                    break;
                    
                case 'h': // int64
                    if ($pos + 8 > $len) {
                        throw new Exception("Unexpected end of data reading int64");
                    }
                    $high = unpack('N', substr($data, $pos, 4))[1];
                    $low = unpack('N', substr($data, $pos + 4, 4))[1];
                    $result['arguments'][] = ($high << 32) | $low;
                    $pos += 8;
                    break;
                    
                case 'd': // double
                    if ($pos + 8 > $len) {
                        throw new Exception("Unexpected end of data reading double");
                    }
                    $packed = substr($data, $pos, 8);
                    $result['arguments'][] = unpack('d', strrev($packed))[1];
                    $pos += 8;
                    break;
                    
                default:
                    echo "Warning: Unknown type tag '$type', skipping\n";
            }
        }
        
        return $result;
    }
    
    /**
     * Align position to 4-byte boundary (OSC requirement)
     */
    private function alignTo4($pos) {
        return ($pos + 3) & ~3;
    }
    
    /**
     * Default message handler
     */
    private function defaultHandler($message, $from, $port) {
        echo "─────────────────────────────────────\n";
        echo "From: $from:$port\n";
        echo "Address: {$message['address']}\n";
        
        if (!empty($message['typetags'])) {
            echo "Types: {$message['typetags']}\n";
        }
        
        if (!empty($message['arguments'])) {
            echo "Arguments:\n";
            foreach ($message['arguments'] as $index => $arg) {
                $type = gettype($arg);
                if (is_string($arg)) {
                    echo "  [$index] (string) \"$arg\"\n";
                } else if (is_float($arg)) {
                    echo "  [$index] (float) $arg\n";
                } else if (is_int($arg)) {
                    echo "  [$index] (int) $arg\n";
                } else if (is_bool($arg)) {
                    echo "  [$index] (bool) " . ($arg ? 'true' : 'false') . "\n";
                } else if (is_null($arg)) {
                    echo "  [$index] (null)\n";
                } else {
                    echo "  [$index] ($type) " . print_r($arg, true) . "\n";
                }
            }
        }
        echo "\n";
    }
    
    /**
     * Close the socket
     */
    public function close() {
        if ($this->socket) {
            socket_close($this->socket);
            echo "Server closed\n";
        }
    }
    
    public function __destruct() {
        $this->close();
    }
}

// ============================================
// Example Usage
// ============================================

try {
    $server = new OSCServer('0.0.0.0', 8000);
    
    // Option 1: Use default handler (displays all messages)
    // $server->listen();
    
    // Option 2: Use custom message handler
    $server->listen(function($message, $from, $port) {
        // Handle specific OSC addresses
        switch ($message['address']) {
            case '/test':
                echo "✓ Test message received from $from:$port\n\n";
                break;
                
            case '/volume':
                if (isset($message['arguments'][0])) {
                    $volume = $message['arguments'][0];
                    echo "🔊 Volume set to: $volume from $from:$port\n\n";
                }
                break;
                
            case '/note':
                if (count($message['arguments']) >= 2) {
                    $note = $message['arguments'][0];
                    $velocity = $message['arguments'][1];
                    echo "♪ Note: $note, Velocity: $velocity from $from:$port\n\n";
                }
                break;
                
            case '/chat':
                if (isset($message['arguments'][0])) {
                    $text = $message['arguments'][0];
                    echo "💬 Chat message: \"$text\" from $from:$port\n\n";
                }
                break;
                
            default:
                // For other messages, use the default display
                echo "📨 Message from $from:$port\n";
                echo "   Address: {$message['address']}\n";
                if (!empty($message['arguments'])) {
                    echo "   Args: " . json_encode($message['arguments']) . "\n";
                }
                echo "\n";
        }
    });
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
    exit(1);
}
