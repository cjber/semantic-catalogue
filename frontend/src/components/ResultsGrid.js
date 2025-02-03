import React from "react";
import {
  Grid,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
} from "@mui/material";
import SourceCard from "./SourceCard";

function ResultsGrid({ results, threadId }) {
  if (!results || Object.keys(results).length === 0) {
    return (
      <Typography
        variant="h6"
        sx={{ p: 2, textAlign: "center", color: "text.secondary" }}
      >
        No results found.
      </Typography>
    );
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography
        variant="h4"
        sx={{ mb: 4, color: "text.primary", textAlign: "center" }}
      ></Typography>
      <Grid container spacing={3}>
        {Object.keys(results).map((source, idx) => (
          <Grid item xs={12} sm={6} md={6} key={idx}>
            <Card
              sx={{
                borderRadius: 2,
                boxShadow: 3,
                overflow: "hidden",
                bgcolor: "background.paper",
              }}
            >
              <CardContent sx={{ p: 2, bgcolor: "background.paper" }}>
                <Typography
                  variant="subtitle1"
                  sx={{ fontWeight: "bold", mb: 2 }}
                >
                  {source}
                </Typography>
                <SourceCard
                  source={source}
                  documents={results[source]}
                  threadId={threadId}
                />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default ResultsGrid;
