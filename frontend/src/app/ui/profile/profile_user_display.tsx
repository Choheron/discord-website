import ClientTimestamp from "../general/client_timestamp"
import { boolToEmoji, formatDateString, onlineStatusToTailwindBgColor } from "@/app/lib/utils"
import CurrentTime from "../general/current_time"

// Display user data in a box
// EXPECTED PROPS:
// - userData: Object [REQUIRED] - User Data object to be passed in, expects data outlined in backend
// - onlineData: Object [REQUIRED] - User Online Data object from backend
export default function ProfileUserDisplay(props) {
  const userData = props.userData
  const last_seen = props.onlineData['last_seen']
  const online = props.onlineData['online']
  const online_status = props.onlineData['status']

  return(
    <div className="w-fit mx-auto lg:max-w-[1080px] flex flex-col gap-2 lg:flex-row backdrop-blur-2xl px-2 py-2 my-2 rounded-2xl bg-zinc-800/30 border border-neutral-800">
      <div className="group">
        <img 
          src={userData['avatar_url']}
          className='h-[125px] w-[125px] lg:h-[200px] lg:w-[200px] rounded-2xl mx-auto'
          alt={`Profile Picture for ${userData['nickname']}`}
        />
        <div className="absolute top-3 left-3 flex bg-black/50 rounded-full pl-2 group-hover:invisible">
          <p>{online_status}</p>
          <div className={`w-[10px] h-[10px] mx-2 my-auto rounded-full border-2 border-black ${onlineStatusToTailwindBgColor(online_status)}`}></div>
        </div>
      </div>
      <div className="flex flex-col justify-between font-extralight">
        <div className="flex flex-col min-w-[350px] max-w-[400px] lg:w-[560px] w-fit">
          <div className="w-full flex justify-between">
            <p>Nickname:</p>
            <p>{userData['nickname']}</p>
          </div>
          <div className="w-full flex justify-between font-extralight">
            <p>Member Since:</p>
            <ClientTimestamp timestamp={formatDateString(userData['creation_timestamp'])}/>
          </div>
          <div className="w-full flex justify-between font-extralight">
            <p>Last Seen:</p>
            <ClientTimestamp timestamp={formatDateString(userData['last_request_timestamp'])} full/>
          </div>
          <div className="w-full flex justify-between font-extralight">
            <p>Time Since Last Seen:</p>
            <p>{last_seen}</p>
          </div>
          <div className="w-full flex justify-between font-extralight">
            <p>Album of the Day Participant:</p>
            <div dangerouslySetInnerHTML={{__html: boolToEmoji(userData['aotd_enrolled'])}}></div>
          </div>
          <div className="w-full flex justify-between font-extralight">
            <p>Current Timezone:</p>
            <p>{userData['timezone_string']}</p>
          </div>
          <div className="w-full flex justify-between font-extralight">
            <p>Current Time:</p>
            <CurrentTime basic={true} timezone={userData['timezone_string']} />
          </div>
        </div>
      </div>
    </div>
  )
}