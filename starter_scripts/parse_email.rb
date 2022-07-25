require 'base64'
require 'json'
require 'net/http'
require 'securerandom'
require 'uri'


thread_id = SecureRandom.urlsafe_base64()
uploader_email_address = 'uploader_email_address@example.com'

post_request_body = { 'emailAddress' => uploader_email_address, 'threadId' => thread_id, 'messages' => [] }

message_1 = File.read("./message_1.txt")

raw_message_list = [ message_1, ]

raw_message_list.each_with_index { |raw_message, index|
    message_uuid = SecureRandom.urlsafe_base64()
    encoded_raw_message = Base64.urlsafe_encode64(raw_message)
    current_message = { 'raw' => encoded_raw_message, 'id' => message_uuid, 'internalDate': index }

    post_request_body['messages'].append(current_message)
}

uri = URI('https://api.fwdeveryone.com/api/v1/thread')
res = Net::HTTP.post(uri, post_request_body.to_json, { "Content-Type" => "application/json" })
puts res.body
