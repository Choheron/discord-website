'use client'

import {
  Modal, 
  ModalContent, 
  ModalHeader, 
  ModalBody, 
  ModalFooter,
  useDisclosure
} from "@nextui-org/modal";
import {
  Table,
  TableHeader,
  TableBody,
  TableColumn,
  TableRow,
  TableCell
} from "@nextui-org/table";
import { Avatar, Button } from "@nextui-org/react";
import React from "react";
import { useRouter } from 'next/navigation';
import { getAllAlbums, getAllAlbumsNoCache } from "@/app/lib/spotify_utils";
import { convertToLocalTZString, ratingToTailwindBgColor } from "@/app/lib/utils";
import Link from "next/link";


// Modal to display all submitted albums
//  - 
export default function AllAlbumsModal(props) {
  const [updateTimestamp, setUpdateTimestamp] = React.useState<any>("")
  const [albumList, setAlbumList] = React.useState([])
  // Sorting variables
  const [sortDescriptor, setSortDescriptor] = React.useState<any>({ column: "rating", direction: "descending"})
  // Modal Controller Vars
  const {isOpen, onOpen, onOpenChange, onClose} = useDisclosure();
  const router = useRouter();
  // Columns for Table
  const columns = [
    {
      key: "title",
      label: "ALBUM NAME",
      sortable: true,
    },
    {
      key: "artist",
      label: "ARTIST",
      sortable: true,
    },
    {
      key: "submitter",
      label: "SUBMITTER",
      sortable: true,
    },
    {
      key: "submission_date",
      label: "SUBMITTED ON",
      sortable: true,
    },
    {
      key: "rating",
      label: "RATING (IF AVAIL)",
      sortable: true,
    },
    {
      key: "AOD_date",
      label: "LAST AOD",
      sortable: true,
    },
    {
      key: "historical_data",
      label: "HISTORICAL DATA",
      sortable: false,
    },
  ];

  // Custom sorting method
  const handleSortChange = (descriptor) => {
    setSortDescriptor(descriptor)
    switch(descriptor.column) {
      // Sort on rating
      case 'rating':
        setAlbumList(albumList.sort((a, b) => {
          if (descriptor.direction === "ascending") return a['rating'] - b['rating'];
          if (descriptor.direction === "descending") return b['rating'] - a['rating'];
          return 0;
        }))
        break;
      // Sort on Submission Date
      case 'submission_date':
        setAlbumList(albumList.sort((a, b) => {
          const dateA: any = new Date(a['submission_date']);
          const dateB: any = new Date(b['submission_date']);
          
          if (descriptor.direction === "ascending") return (dateA - dateB);
          if (descriptor.direction === "descending") return (dateB - dateA);
          return 0;
        }))
        break;
      // Sort on Submitter Nickname
      case 'submitter':
        setAlbumList(albumList.sort((a, b) => {
          if (descriptor.direction === "ascending") return ((a['submitter_nickname'] < b['submitter_nickname']) ? 1 : -1);
          if (descriptor.direction === "descending") return ((a['submitter_nickname'] > b['submitter_nickname']) ? 1 : -1);
          return 0;
        }))
        break;
      // Sort on Artist Name
      case 'artist':
        setAlbumList(albumList.sort((a, b) => {
          if (descriptor.direction === "ascending") return ((a['artist']['name'] < b['artist']['name']) ? 1 : -1);
          if (descriptor.direction === "descending") return ((a['artist']['name'] > b['artist']['name']) ? 1 : -1);
          return 0;
        }))
        break;
      // Sort on Album Title
      case 'title':
        setAlbumList(albumList.sort((a, b) => {
          if (descriptor.direction === "ascending") return ((a['title'] < b['title']) ? 1 : -1);
          if (descriptor.direction === "descending") return ((a['title'] > b['title']) ? 1 : -1);
          return 0;
        }))
        break;
      // Sort on Last Album of Day Date
      case 'AOD_date':
        setAlbumList(albumList.sort((a, b) => {
          if (descriptor.direction === "ascending") return ((a['AOD_date'] < b['AOD_date']) ? 1 : -1);
          if (descriptor.direction === "descending") return ((a['AOD_date'] > b['AOD_date']) ? 1 : -1);
          return 0;
        }))
        break;
    }
  };

  // UseEffect to pull Album Data
  React.useEffect(() => {
    const ingestData = async () => {
      let albumData = await getAllAlbums()
      setAlbumList(albumData['albums_list'])
      setUpdateTimestamp(albumData['timestamp'])
    }
    ingestData()
  }, [])

  // Render Cell dynamically
  const renderCell = React.useCallback((album , columnKey: React.Key) => {
    // Change render based on column key
    switch (columnKey) {
      case "title":
        return (
          <div className="flex gap-2">
            <Avatar
              src={album['album_img_src']}
            />
            <a href={album['album_src']} target="_noreferrer" className="text-lg my-auto hover:underline">
              {album['title']}
            </a>
          </div>
        );
      case "artist":
        return (
          <a href={album['artist']['href']} target="_noreferrer" className="w-fit text-md my-auto hover:underline">
            {album['artist']['name']}
          </a>
        );
      case "submitter":
        return (
          <div className="flex gap-2">
            <Avatar
              src={album['submitter_avatar_url']}
            />
            <p className="my-auto">
              {album['submitter_nickname']}
            </p>
          </div>
        );
      case "submission_date":
        return (
          <p className="my-auto">
            {album['submission_date']}
          </p>
        );
      case "rating":
        return (
          (album['rating'] != null)? 
            <div className={`px-2 py-2`}>
              <p className={`text-center text-black ${ratingToTailwindBgColor(album['rating'])} rounded-full`}>
                <b>{album['rating'].toFixed(2)}</b>
              </p>
            </div> 
            : 
            <p className="text-center">
              --
            </p>
        );
      case "AOD_date":
          return (
            <p className="my-auto">
              {(album['AOD_date'] != null) ? album['AOD_date'] : "N/A"}
            </p>
          );
      case "historical_data":
            return (
              (album['AOD_date'] != null) ? (
                <Button 
                  as={Link}
                  href={"/dashboard/spotify/historical/" + album['AOD_date']}
                  radius="lg"
                  className={`w-fit mx-auto hover:underline text-white`}
                  variant="solid"
                >
                  <b>View Historical Data</b>
                </Button> 
              ):(
                <></>
              )
            );
    }
  }, []);

  // Reset values on cancel button press
  const hardRefresh = () => {
    const ingestNewData = async () => {
      let albumData = await getAllAlbumsNoCache()
      setAlbumList(albumData['albums_list'])
      setUpdateTimestamp(albumData['timestamp'])
    }
    ingestNewData()
  }

  // Reset values on cancel button press
  const cancelPress = () => {
    onClose()
    // Reload page
    router.refresh()
  }

  return (
    <>
      <Button 
        className="p-2 mx-auto my-2 w-[90%] text-sm text-inheret h-fit hover:underline"
        size="sm"
        onPress={onOpen}
        radius="lg"
        variant="solid"
      >
        View All Albums
      </Button>
      <Modal 
        size="5xl" 
        scrollBehavior={"inside"}
        isOpen={isOpen} 
        onOpenChange={onOpenChange} 
        backdrop="blur"
        onClose={cancelPress}
        classNames={{
          base: "max-w-full lg:max-w-[75%]",
        }}
      >
        <ModalContent>
          {() => (
            <>
              <ModalHeader className="flex flex-col flex-wrap w-full gap-1 content-center">
                Album Data
              </ModalHeader>
              <ModalBody>
                <Table 
                  aria-label="Album Submissions"
                  sortDescriptor={sortDescriptor}
                  onSortChange={handleSortChange}
                  isStriped
                >
                  <TableHeader columns={columns}>
                    {(column) =>
                      <TableColumn key={column.key} allowsSorting={column.sortable} className="w-fit">{column.label}</TableColumn>
                    }
                  </TableHeader>
                  <TableBody 
                    items={albumList}
                    emptyContent={"No rows to display."}
                  >
                    {(item) => (
                      <TableRow key={item['title']}>
                        {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </ModalBody>
              <ModalFooter>
                <div className="flex w-full justify-between">
                  <p className="my-auto">
                    Data Last Updated: {convertToLocalTZString(updateTimestamp, true)}
                  </p>
                  <div>
                    <Button color="primary" variant="solid" className="mr-2" onPress={hardRefresh}>
                      Hard Refresh
                    </Button>
                    <Button color="danger" variant="bordered" onPress={onClose}>
                      Close
                    </Button>
                  </div>
                </div>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  )
}