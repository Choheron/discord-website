'use server'

import Image from 'next/image'

import { Conditional } from "../conditional"
import UserCard from '../../general/userUiItems/user_card';
import StarRating from '../../general/star_rating';

// GUI Display for an Album
// Expected Props:
//  - title: String - Title of the Album
//  - album_img_src: string - Url to access the album image [EXTERNAL]
//  - album_src: string - Url for user to access the album [EXTERNAL]
//  - artist: Object - Object of Artist Data (Expected fields in object below)
//      > name: String - Name of Artist
//      > href: String - Url to access artist on spotify [EXTERNAL URL]
//  - submitter: String - (Optional) The discord id of the user that submitted this album, not applicable in all use cases
//  - submitter_comment: String - (Optional) An optional comment that the album submitter may have left with this album
//  - submission_date: String - (Optional) A String representation of the submission date of the Album
//  - avg_rating: Int - Average rating of album by site users who have authenticated
export default async function AlbumDisplay(props) {
  // Album props checks
  const title = (props.title) ? props.title : "No Album Title Found";
  const album_url = (props.album_src) ? props.album_src : "https://www.google.com/search?q=sad+face";
  const album_img_src = (props.album_img_src) ? props.album_img_src : "/images/DALL-E_Album_Not_Found.webp";
  // Artist props checks
  const artist_name = (props.artist && props.artist['name']) ? props.artist['name'] : "Artist Name not Found";
  const artist_url = (props.artist && props.artist['href']) ? props.artist['href'] : "https://www.google.com/search?q=sad+face";
  // User rating props checks
  const submitter = (props.submitter) ? props.submitter : "Not Provided";
  const submitter_comment = (props.submitter_comment) ? props.submitter_comment : "No Comment Provided";
  const submission_date = (props.submission_date) ? props.submission_date : "Not Provided";
  // Rating props check
  const avg_rating = (props.avg_rating) ? props.avg_rating : 0;

  return (
    <div className="w-full min-w-[320px] mx-2 lg:mx-1 my-2 flex flex-col lg:flex-row">
      <Image
        src={album_img_src}
        width={320}
        height={320}
        alt={`Album Cover for ${title} by ${artist_name}`}
        className={'h-[300px] w-[300px] rounded-2xl mx-auto'}
      />
      <div className="w-full flex flex-col gap-2 pl-5 pt-2 my-auto">
        <a href={album_url} target="_noreferrer" className="text-3xl hover:underline">
          {title}
        </a>
        <a href={artist_url} target="_noreferrer" className="text-xl hover:underline italic">
          {artist_name}
        </a>
        <Conditional showWhen={props.submitter}>
          <div className="">
            <p>Submitted By: </p>
            <div className="ml-2 -mb-1">
              <UserCard userDiscordID={submitter} fallbackName={"User Not Found"}/>
            </div>
            <p>On: <i>{submission_date}</i></p>
          </div>
        </Conditional>
        <Conditional showWhen={(avg_rating != 0)}>
          <div className="">
            <p>Average User Rating: </p>
            <div className="ml-2">
              <StarRating 
                className="text-yellow-400 text-xl"
                rating={avg_rating} 
              />
            </div>
          </div>
        </Conditional>
      </div>
    </div>
  )
}