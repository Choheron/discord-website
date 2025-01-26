'use server'

import { Conditional } from "../conditional"
import {Popover, PopoverTrigger, PopoverContent} from "@nextui-org/popover";
import UserCard from '../../general/userUiItems/user_card';
import StarRating from '../../general/star_rating';
import { getAlbumAvgRating } from '@/app/lib/spotify_utils';
import { Button } from "@nextui-org/react";
import Link from "next/link";
import { ratingToTailwindBgColor } from "@/app/lib/utils";
import ClientTimestamp from "../../general/client_timestamp";

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
//  - album_spotify_id: String - (Optional) Album Spotify ID for retrieval of average from database
//  - historical_date: String - (Optional) Date in which this album was Album Of the Day (THIS IS FOR HISTORICAL DISPLAYS)
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
  const submission_date: string = (props.submission_date) ? props.submission_date : "Not Provided";
  // Rating props check
  const avg_rating = (props.album_spotify_id) ? await getAlbumAvgRating(props.album_spotify_id, false): 0.0;
  // Historical props checks
  const historical = (props.historical_date) ? true : false;
  const historical_date = (props.historical_date) ? props.historical_date : "0000-00-00";

  return (
    <div className="w-full min-w-[320px] lg:min-w-[650px] mx-2 lg:mx-1 my-auto flex flex-row">
      <img 
        src={album_img_src}
        className='h-[125px] w-[125px] lg:h-[300px] lg:w-[300px] rounded-2xl mx-auto'
        alt={`Album Cover for ${title} by ${artist_name}`}
      />
      <div className="w-full flex flex-col lg:gap-2 pl-2 lg:pl-5 pt-1 lg:pt-2 my-auto">
        <a href={album_url} target="_noreferrer" className="text-xl lg:text-3xl hover:underline">
          {title}
        </a>
        <a href={artist_url} target="_noreferrer" className="text-sm lg:text-xl hover:underline italic">
          {artist_name}
        </a>
        <Conditional showWhen={props.submitter}>
          <div className="">
            <p>Submitter: </p>
            <div className="ml-2 -mb-1">
              <Popover placement="left" showArrow={true} className="w-fit">
                <PopoverTrigger>
                  <div>
                    <UserCard userDiscordID={submitter} fallbackName={"User Not Found"}/>
                  </div>
                </PopoverTrigger>
                <PopoverContent>
                  <p>{submitter_comment}</p>
                </PopoverContent>
              </Popover>
            </div>
            <div className="flex">
              <p>Submission Date:</p>
              <ClientTimestamp className="italic pl-1" timestamp={submission_date} full={false}/>
            </div>
          </div>
        </Conditional>
        <Conditional showWhen={(avg_rating != 0) && ((avg_rating != null))}>
          <div className="">
            <div className="flex mb-1">
              <p>Average User Rating: </p>
              <p className={`ml-2 px-2 rounded-xl text-black ${ratingToTailwindBgColor(avg_rating)}`}>
                <b>{avg_rating.toFixed(2)}</b>
              </p>
            </div>
            <div className="ml-2">
              <StarRating 
                className="text-yellow-400 text-xl"
                rating={avg_rating} 
                textSize="text-2xl lg:text-4xl"
              />
            </div>
          </div>
        </Conditional>
        <Conditional showWhen={historical}>
          <Button 
            as={Link}
            href={"/dashboard/spotify/historical/" + historical_date}
            radius="lg"
            className={`w-fit hover:underline text-white`}
            variant="solid"
          >
            <b>All Reviews</b>
          </Button> 
        </Conditional>
      </div>
    </div>
  )
}