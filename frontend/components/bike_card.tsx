'use client'
import React from "react";
import { Card, CardHeader, CardBody, CardFooter, Image, Button } from "@nextui-org/react";

export default function BikeCard({ bikeName, postDate, listingUrl, imageUrl }) {
  return (
    <div className="max-w-[900px] gap-2 grid grid-cols-12 grid-rows-2 px-8">
      <Card isFooterBlurred className="w-full h-[300px] col-span-12 sm:col-span-7">
        <CardHeader className="absolute z-10 top-1 flex-col items-start">
          <p className="text-tiny text-white/60 uppercase font-bold">New Listing</p>
          <h4 className="text-white/90 font-medium text-xl">{bikeName}</h4>
        </CardHeader>
        <Image
          removeWrapper
          alt="Bike image"
          className="z-0 w-full h-full object-cover"
          src={imageUrl}
        />
        <CardFooter className="absolute bg-black/40 bottom-0 z-10 border-t-1 border-default-600 dark:border-default-100">
          <div className="flex flex-grow justify-between items-center">
            <div className="flex flex-col">
              <p className="text-tiny text-white/60">Posted: {postDate}</p>
            </div>
            <Button 
              radius="full" 
              size="sm" 
              onPress={() => window.open(listingUrl, "_blank")}
            >
              View Listing
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
