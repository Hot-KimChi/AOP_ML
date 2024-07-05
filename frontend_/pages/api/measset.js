export default function handler(req, res) {
  res.status(200).json({
    id: 1,
    name: "Sample MeasSet",
    description: "This is a sample MeasSet"
  })
}