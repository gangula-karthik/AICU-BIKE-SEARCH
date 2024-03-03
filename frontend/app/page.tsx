import { Link } from "@nextui-org/link";
import { Snippet } from "@nextui-org/snippet";
import { Code } from "@nextui-org/code"
import { button as buttonStyles } from "@nextui-org/theme";
import { siteConfig } from "@/config/site";
import { title, subtitle } from "@/components/primitives";
import { GithubIcon } from "@/components/icons";
import BikeCard from "../components/bike_card";
import { Textarea, Input, Button } from "@nextui-org/react";
import { Popover, PopoverTrigger, PopoverContent } from "@nextui-org/react";
import { UploadOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { Upload } from 'antd';
import type { UploadFile } from 'antd';


export default function Home() {
	const bikeInfo = {
		bikeName: "Mountain Bike Pro",
		postDate: "2022-09-01",
		listingUrl: "https://www.example.com/bike-listing",
		imageUrl: "https://www.example.com/images/bike.jpg",
	};


	const fileList: UploadFile[] = [
		{
			uid: '-1',
			name: 'yyy.png',
			status: 'done',
			url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
			thumbUrl: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
		}
	];

	const content = (
		<PopoverContent>
			<Upload
				action="https://run.mocky.io/v3/435e224c-44fb-4773-9faf-380c5e6a2188"
				listType="picture"
				defaultFileList={[...fileList]}
			>
				<Button icon={<UploadOutlined />}>Upload</Button>
			</Upload>
			<br />
		</PopoverContent>
	);


	return (
		<section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
			<div className="inline-block max-w-lg text-center justify-center">
				<h1 className={title()}>Empower&nbsp;</h1>
				<h1 className={title({ color: "violet" })}>your cycling journey&nbsp;</h1>
				<br />
				<h2 className={subtitle({ class: "mt-4" })}>
					Revolutionizing bike recovery with state-of-the-art AI technology.
				</h2>
			</div>

			<div className="w-full grid grid-cols-12 gap-4">
				<Input
					key="bordered"
					color='secondary'
					variant="bordered"
					placeholder="Enter the bike description here. A template you can follow is -> '[Brand name] is in [condition]. [Description].'
					"
					className="col-span-15 md:col-span-10 mb-6 md:mb-0"
				/>
			</div>
			<Button color="secondary" variant="shadow">
				Send
			</Button>

			<div className="flex flex-wrap gap-4">

				<Popover key="secondary" placement="top" color="secondary">
					<PopoverTrigger>
						<Button color="secondary" className="capitalize">
							+ Upload Image
						</Button>
					</PopoverTrigger>
					{content}
				</Popover>
			</div>

			<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
				<BikeCard {...bikeInfo} />
			</div>
		</section>
	);
}
