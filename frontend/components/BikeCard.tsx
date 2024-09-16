"use client"

interface BikeCardProps {
  imageUrl: string;
  bikeName: string;
  description: string;
  source: string;
}


import React from 'react';
import { Card, CardHeader, CardFooter, Image, Button, Chip, Link, Tooltip } from '@nextui-org/react';

const BikeCard: React.FC<BikeCardProps> = ({ imageUrl, bikeName, description, source }) => {
  return (
    <Card isFooterBlurred className="w-[400px] h-[250px]">
      <Tooltip showArrow={true} color='primary' delay={0}
        closeDelay={0}
        placement="top-start"
        motionProps={{
          variants: {
            exit: {
              opacity: 0,
              transition: {
                duration: 0.1,
                ease: "easeIn",
              }
            },
            enter: {
              opacity: 1,
              transition: {
                duration: 0.15,
                ease: "easeOut",
              }
            },
          },
        }} content={
          <div className="px-1 py-2">
            <div className="text-tiny">{bikeName}</div>
          </div>
        }>
        <Image
          removeWrapper
          alt={bikeName}
          className="z-0 w-full h-full object-cover"
          src={imageUrl}
        />
      </Tooltip>
      <CardFooter className="absolute bg-black/40 bottom-0 z-10 border-t-1 border-default-600">
        <div className="flex flex-grow gap-2 items-center">
          <div className="flex flex-col">
            <p className="text-tiny text-white/60">{description}</p>
          </div>
        </div>
        <Button as={Link} href={source} color="primary" radius="full" size="sm">View It 🚀</Button>
      </CardFooter>
    </Card>
  );
};

export default BikeCard;