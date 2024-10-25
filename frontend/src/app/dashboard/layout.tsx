import "@/app/globals.css";
import TopBar from "../ui/dashboard/top_bar";
import { isMember } from "../lib/discord_utils";
import { getUserData, getUserAvatarURL } from "../lib/user_utils";



export default async function Layout({ children }: { children: React.ReactNode }) {
  // Retrieve user data
  const userData = await getUserData();
  const memberStatus = await isMember();
  const avatarURL = await getUserAvatarURL();

  return (
    <div>
      <TopBar userInfo={userData} isMember={memberStatus} avatarURL={avatarURL}/>
      {children}
    </div>
  );
}
