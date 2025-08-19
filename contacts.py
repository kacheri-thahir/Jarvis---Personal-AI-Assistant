import pywhatkit as pwk


contacts={
        "" #Add your contacts list here...
}
    

def send_whatsapp_message(request):
    if "send message" in request:
        try:
            message_part=request.split("message")[1].strip()
            if 'to' in message_part:
                message_text= message_part.split('to')[0].strip()
                contact_name= message_part.split('to')[1].strip()

                if contact_name in contacts:
                    phone=contacts[contact_name]
                    pwk.sendwhatmsg_instantly(phone, message_text,wait_time=10,tab_close=True)
                    print(f"Message sent to {contact_name}")
                else:
                    print("contact not found.")
            else:
                print("Please specify the contact name after 'to'.")
        except Exception as e:
            print(f"Error: {e}")

