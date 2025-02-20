import React from "react";
import { Box, Text } from "@mantine/core";
import { motion } from "framer-motion";


const EllipsisLoader = () => {
  const text = "Ejecutando query";
  return (
    <Box style={{ display: "flex", alignItems: "center", gap: "4px" }}>
      <Text>
        {text.split("").map((char, i) => (
          <motion.span
            key={i}
            initial={{ opacity: 0 }}
            animate={{ opacity: 3 }}
            transition={{ delay: i * 0.1, duration: 1.2, repeat: Infinity, repeatDelay: 0.8, repeatType:"reverse" }}
          >
            {char}
          </motion.span>
        ))}
      </Text>
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          style={{ width: "4px", height: "4px", backgroundColor: "#4A4A4A", borderRadius: "50%", "marginTop":'5px', 'marginLeft':'2px' }}
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{
            repeat: Infinity,
            duration: 1.2,
            delay: i * 0.3,
          }}
        />
      ))}
    </Box>
  );
};
export default EllipsisLoader;